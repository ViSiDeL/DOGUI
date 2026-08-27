from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, g

from api.models.inference import generate_text
from src.api.models.session import login_required
from src.api.models.project import ProjectService
from src.api.models.prompt import build_chat_prompt
from src.api.models.history import ChatHistoryService

ai_bp = Blueprint('ai', __name__)

""" ------------------- ASSISTANT INFO ------------------- """
languages = {
    "English": "en-US_MichaelV3Voice",
    "Japanese": "ja-JP_EmiV3Voice",
    "Arabic": "ar-AR_OmarV3Voice",
    "Spanish":"es-ES_EnriqueV3Voice",
    "French":"fr-FR_ReneeV3Voice",
    "Dutch":"nl-NL_MerelV3Voice",
    "German": "de-DE_DieterV3Voice"
}

""" ------------------- LLM USAGE ------------------- """

@ai_bp.route('/assistant')
@login_required
def assistant():
    project_id = request.args.get('project_id')
    context_type = request.args.get('context', '').lower()
    project_context = None

    if project_id:
        try:
            project_id = int(project_id)
            user = g.user
            project_data = ProjectService.get_project_with_contexts(project_id, user.username)
            if not project_data:
                flash('Project not found', 'error')
                return redirect(url_for('project.projects'))

            previous_context = session.get('current_project') or {}
            if previous_context.get('id') != project_data['ID']:
                ChatHistoryService.clear_history(user.username)

            project_context = {
                'id': project_data['ID'],
                'name': project_data['projectName'],
                'description': project_data['description'],
                'contexts': project_data.get('contexts', '') or '',
                'context_type': context_type,
                'username': user.username
            }
            session['current_project'] = project_context
        except Exception as e:
            print(f"Error loading project context: {e}")
            session.pop('current_project', None)
            project_context = None

    return render_template('assistant.html', project_context=project_context)

@ai_bp.route('/chatbot', methods=['POST'])
@login_required
def chatbot():
    data = request.get_json()
    user_message = data.get('message')
    voice_choice = data.get('voice')  # frontend must send this

    if not user_message:
        return jsonify({'response': 'No message received.'})

    try:
        user = g.user
        project_context = session.get('current_project', {})
        
        base_prompt = build_chat_prompt(project_context, user_message)
        history_text = ChatHistoryService.as_prompt_text(user.username)
        full_prompt = f"{history_text}\n\n{base_prompt}" if history_text else base_prompt

        response = generate_text(prompt=full_prompt)

        ChatHistoryService.add_message(user.username, 'user', user_message)
        ChatHistoryService.add_message(user.username, 'assistant', response)

        # voice_choice handling (optional, kept for compatibility)
        # voice_choice = voice_choice.capitalize()
        # if voice_choice not in languages:
        #     return jsonify({'response': response, 'error': 'Invalid voice choice.'})
        # converted_voice_choice = languages[voice_choice]

        return jsonify({
                'response': response,
                'project_context': project_context.get('name'),
                'audio_url': ''
            })
    except Exception as e:
        print(f"Error in chatbot response: {e}")
        return jsonify({'response': 'Error generating response. Please try again.'})


@ai_bp.route('/chatbot/history')
@login_required
def chatbot_history():
    return jsonify({'history': ChatHistoryService.get_history(g.user.username)})


@ai_bp.route('/chatbot/clear', methods=['POST'])
@login_required
def chatbot_clear():
    ChatHistoryService.clear_history(g.user.username)
    return jsonify({'success': True})


""" ------------------- IDEATION ------------------- """

@ai_bp.route('/generate-project-name', methods=['POST'])
@login_required
def generate_project_name():
    try:
        data = request.get_json()
        description = data.get('description')

        if not description:
            return jsonify({'error': 'No description provided'}), 400

        prompt = f"""
        Generate a concise, professional project name (2-4 words max) based on this description:
        "{description}"

        Respond ONLY with the project name, no additional text or explanations.
        Try to make the name trendy, unique, but still short and descriptive. You can add spaces if necessary.
        Project Name:
        """

        response = generate_text(prompt=prompt)
        project_name = response.strip().strip('"').strip("'")

        return jsonify({'project_name': project_name})

    except Exception as e:
        print(f"Error generating project name: {e}")
        return jsonify({'error': 'Failed to generate project name'}), 500

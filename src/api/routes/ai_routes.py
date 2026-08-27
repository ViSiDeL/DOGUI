import os

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
import pymysql

from api.models.inference import generate_text
from engine_instance import design_engine

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
def assistant():
    project_id = request.args.get('project_id')
    context_type = request.args.get('context', '').lower()
    project_context = None

    if project_id:
        try:
            project_id = int(project_id)

            # verify user has access to this project
            session_id = session.get('session_id')
            if not session_id:
                return redirect(url_for('user.login'))

            user = design_engine.get_user(session_id)
            if not user:
                return redirect(url_for('user.login'))


            connection = pymysql.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_DATABASE'),
                port=int(os.getenv('DB_PORT'))
            )

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(
                    """SELECT p.ID, p.projectName, p.description,
                    GROUP_CONCAT(c.context_text SEPARATOR '\n') AS contexts
                    FROM projects p
                    LEFT JOIN contexts c ON p.ID = c.project_id
                    WHERE p.ID = %s AND p.username = %s
                    GROUP BY p.ID""",
                    (project_id, user.username)
                )
                project_data = cursor.fetchone()

            if not project_data:
                flash('Project not found', 'error')
                print('Project not found')
                return redirect(url_for('project.projects'))

            # store in session for chatbot to access
            project_context = {
                'id': project_data['ID'],
                'name': project_data['projectName'],
                'description': project_data['description'],
                'contexts': project_data['contexts'] or '',
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
def chatbot():
    data = request.get_json()
    user_message = data.get('message')
    voice_choice = data.get('voice')  # frontend must send this

    if not user_message:
        return jsonify({'response': 'No message received.'})

    try:
        project_context = session.get('current_project', {})

        # build context-aware prompt
        context_prompt = ""
        if project_context:
            context_prompt = f"""
            Current Project: {project_context.get('name', 'N/A')}
            Project Description: {project_context.get('description', 'None provided')}
            Additional Context: {project_context.get('contexts', 'None')}
            Current Task: {project_context.get('context_type', 'General inquiry')}
            """

        full_prompt = f"""
        You are DOGUI AI, an engineering-focused assistant. Act as a professional engineer helping another engineer to complete their projects.
        Here's the current context: {context_prompt}.

        Response Guidelines:
        - Focus on the Engineering Design Process (Ideation, Simulation, Implementation)
        - Consider the project context above. If a task is given try to stay on task while still answering the users prompts
        - Provide detailed, actionable advice. Guide the user through the project creation process if needed
        - Ask clarifying questions when needed. Try to be clear and concise, get your point across to the user quickly
        - DO NOT RESPOND IN a numerical LIST FORMAT. You are having a conversation
        - You can provide exact information, as the user may use you for research purposes
        - Keep things simple. Short and sweet.
        - Feel free to provide outside info that a user inquires about.
        - Priortize making sure your response helps the user towards their goal in someway.
        - Keep things simple. Short and sweet.

        The user asks: "{user_message}"

        Your response:
        """

        response = generate_text(prompt=full_prompt)

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
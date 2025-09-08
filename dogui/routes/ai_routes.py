from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from difflib import get_close_matches
from typing import Optional
import pymysql
import json
import time
import random
import string
import os

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1
from ibm_watson import SpeechToTextV1
import speech_recognition as sr
from engine_instance import design_engine


ai_bp = Blueprint('ai', __name__)

# loading db config
def load_db_config():
    with open('config/db_connection.json') as config_file:
        return json.load(config_file)

""" WATSON SETUP """
# loading watson apikey
def load_watson_config():
    with open('config/watson_info.json') as watson_config_file:
        return json.load(watson_config_file)
    
# watson setup
watson_config = load_watson_config() 
credentials = Credentials(
    url = watson_config['url'],
    api_key = watson_config['IBM_API_KEY']
)
chatbot_model = ModelInference(
    model_id=watson_config['model_id'],
    credentials=credentials,
    project_id=watson_config['project_id'],
    params= {
		"decoding_method": "greedy",
		"max_new_tokens": 900,
		"min_new_tokens": 0,
		"repetition_penalty": 1
	},
)
print("Watson Connection Built.")

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
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)
        return data
    
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> Optional[str]:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None 

def get_answer_for_question(question: str, knowledge_base: dict) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None  

""" ------------------- LLM USAGE ------------------- """


# assistant 
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
            
            db_config = load_db_config()
            connection = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                port=int(db_config['port'])
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
                
            # print(project_data)

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
        knowledge_base = load_knowledge_base('config/knowledge_base.json')

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
        - Priortize making sure your response helps the user towards their goal in someway. 
        - Feel free to provide outside info that a user inquires about.
        - Keep things simple. Short and sweet.
        
        The user asks: "{user_message}"

        Your response:
        """
        
        response = chatbot_model.generate_text(prompt=full_prompt)
        # print(response)

        # Voice choice handling
        voice_choice = voice_choice.capitalize()
        if voice_choice not in languages:
            return jsonify({'response': response, 'error': 'Invalid voice choice.'})
        converted_voice_choice = languages[voice_choice]

        # Watson TTS setup
        authenticator = IAMAuthenticator(watson_config['IBM_API_KEY'])
        text_to_speech = TextToSpeechV1(authenticator=authenticator)
        text_to_speech.set_service_url(watson_config['texttospeech_url'])
        
        # Clean up previous audio file if exists
        previous_audio = session.get('audio_filename')
        if previous_audio and os.path.exists(os.path.join('static/audio', previous_audio)):
            os.remove(os.path.join('static/audio', previous_audio))
        
        # Create a unique filename using timestamp and random string
        unique_filename = f"dogui_audio_{int(time.time())}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}.wav"
        output_filename = os.path.join('static/audio', unique_filename)

        audio = text_to_speech.synthesize(
            text=response,
            voice=converted_voice_choice,
            accept='audio/wav'
        ).get_result().content

        if not os.path.exists('static/audio'):
            os.makedirs('static/audio')

        with open(output_filename, 'wb') as f:
            f.write(audio)
        
        session['audio_filename'] = unique_filename

        return jsonify({
                'response': response,
                'project_context': project_context.get('name'),
                'audio_url': f'/' + output_filename
            })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'An error occurred while processing your request.'})

""" ------------------- IDEATION ------------------- """
@ai_bp.route('/generate-project-name', methods=['POST'])
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
        
        response = chatbot_model.generate_text(prompt=prompt)
        project_name = response.strip().strip('"').strip("'")
        
        return jsonify({'project_name': project_name})
        
    except Exception as e:
        print(f"Error generating project name: {e}")
        return jsonify({'error': 'Failed to generate project name'}), 500
    

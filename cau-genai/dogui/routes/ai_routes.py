from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from difflib import get_close_matches
from typing import Optional
import json

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

ai_bp = Blueprint('ai', __name__)

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

""" ------------------- KNOWLEDGE BASE ------------------- """
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

# loading assistant page
@ai_bp.route('/assistant', methods=['GET'])
def assistant():
    return render_template('assistant.html')

# handles responses from watson
@ai_bp.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'response': 'No message received.'})
    try:
        knowledge_base: dict = load_knowledge_base('config/knowledge_base.json')

        # get response, process as needed
        prompt = f"{user_message}"
        full_prompt=f"""
        You are DOGUI AI, an engineering-focused AI assistant meant to create a very descriptive response based of the users question to guide them through their given engineering projects and ideas.
        Your primary purpose is to craft highly vivid, engaging, and richly detailed responses based on the user's questions.
        Especially promote the three steps Ideation, Simulation, and Design of the Engineerin Design Process and a guide a user accordingly
        Here is their message"{prompt}". Your response:"""

        response = chatbot_model.generate_text(prompt=full_prompt)

        reply = response
        return jsonify({'response': reply})

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
        
        Respond ONLY with the project name, no additional text or explanations. Project Name:
        """
        
        response = chatbot_model.generate_text(prompt=prompt)
        project_name = response.strip().strip('"').strip("'")
        
        return jsonify({'project_name': project_name})
        
    except Exception as e:
        print(f"Error generating project name: {e}")
        return jsonify({'error': 'Failed to generate project name'}), 500
    

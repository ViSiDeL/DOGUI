from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import json

ai_bp = Blueprint('ai', __name__)

# loading assistant page
@ai_bp.route('/assistant', methods=['GET'])
def assistant():
    return render_template('design/assistant.html')

# TODO use ibm watson resources to handle speech to text, sending text to watson ai, getting response, and using text to speech to play response
@ai_bp.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'response': 'No message received.'})

    try:
        # get response, process as needed
        response = None

        reply = "Chat has not been implemented yet"
        return jsonify({'response': reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'An error occurred while processing your request.'})

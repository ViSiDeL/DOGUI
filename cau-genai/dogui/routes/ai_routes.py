from flask import Blueprint, render_template, request, redirect, url_for, flash
import json

ai_bp = Blueprint('ai', __name__)

# loading assistant page
@ai_bp.route('/assistant', methods=['GET'])
def assistant():
    return render_template('design/assistant.html')

# TODO use ibm watson resources to handle speech to text, sending text to watson ai, getting response, and using text to speech to play response
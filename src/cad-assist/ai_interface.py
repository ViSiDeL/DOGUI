import json
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from datetime import datetime
from routes.cad_assist.scripts.generated_script import save_script_to_file  # Importing from generated_script
import re

# Load Watson configuration
def load_watson_config():
    with open('config/watson_info.json') as f:
        return json.load(f)

watson_config = load_watson_config()

credentials = Credentials(
    url=watson_config["url"],
    api_key=watson_config["IBM_API_KEY"]
)

model = ModelInference(
    model_id=watson_config["model_id"],
    credentials=credentials,
    project_id=watson_config["project_id"],
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 1500,
        "min_new_tokens": 100,
        "repetition_penalty": 1.1
    }
)

def clean_response(raw_code):
    # Remove any unwanted markers like instructions and response labels
    raw_code = raw_code.replace('### Instruction:', '')  # Remove instructions
    raw_code = raw_code.replace('### Response:', '')  # Remove response labels
    raw_code = raw_code.strip()  # Clean up leading and trailing spaces

    # Optionally, remove other unwanted parts like extra symbols or irrelevant text
    raw_code = raw_code.replace('***INSTRUCTION', '')  # Remove any instructions
    raw_code = raw_code.replace('***TASK', '')  # Remove any tasks

    # Make sure it's clear and ready for display (cleaning any remaining stray characters)
    raw_code = raw_code.replace('\n', ' ').strip()  # Flatten any newlines for better readability

    return raw_code


# Function to start an interactive conversation with the AI
# def call_ai_model(prompt: str, history: list = None) -> str:
#     history = history or []

#     # Conversation-based prompt flow to guide design
#     full_prompt = f"""
#     You are Dogui CAD Assistant, an AI that helps engineers and students refine and design 2D and 3D CAD drawings.

#     Based on the users description ask the user questions and use the answers to help guide them through the design process.

#     The user will describe what they want to design, and you should ask the necessary questions to gather relevant details.
#     You can also give feedback on their design and ask for clarifications.

#     Here is the user's design description: {prompt}

#     Please engage the user interactively and guide them through the design process. Do not include "***RESPONSE" OR "***INSTRUCTIONS" in your response:

#     Your response: " "
#     """

#     history.append(full_prompt + "\n")

#     try:
#         response = model.generate_text(full_prompt)
#         clean = clean_response(response)
#         history.append(response + "\n")
#         document_prompt(history)  # Document the conversation history for later reference
#         return clean  # Return the interactive response (feedback or question)
#     except Exception as e:
#         print(f"❌ Error generating response: {e}")
#         return "# AI generation failed. Please try again."

def call_ai_model(history: list) -> str:
    # Join the conversation history into a single string for the AI model
    full_prompt = "\n".join(history)  # Use the entire conversation history
    
    full_prompt += "\nHow can Dogui CAD assist help?"  # Optional: AI asks first question for new conversations
    
    try:
        response = model.generate_text(full_prompt)
        clean = clean_response(response)
        return clean
    except Exception as e:
        print(f"❌ Error generating response: {e}")
        return "# AI generation failed. Please try again."


def document_prompt(history: list):
    directory = os.path.join(os.path.dirname(__file__), 'templates', 'documents')
    os.makedirs(directory, exist_ok=True)
    filename = "documentation.txt"
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as file:
        file.write("".join(history))
        print(f"{filename} saved to {filepath}.")


'''
Example prompt:
Based on our conversation, generate a Python script using the pyautocad library that creates the requested object(s) in AutoCAD.

Object: Square
Width: 10 feet
Height: 10 feet
Material: Wood

Please initialize AutoCAD using pyautocad, create the drawing using model space, and include comments in the code for readability.

'''


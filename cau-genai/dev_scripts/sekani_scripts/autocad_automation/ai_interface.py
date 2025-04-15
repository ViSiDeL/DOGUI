import json
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from datetime import datetime

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
        "max_new_tokens": 1500,   # Increase max tokens to allow more output
        "min_new_tokens": 100,
        # "temperature": 0.3,       # Lower for more factual/controlled output
        "repetition_penalty": 1.1
    }
)
def clean_response(raw_code):
    for marker in ['```python', '```', '***INSTRUCTION', '***TASK', '***RESPONSE']:
        raw_code = raw_code.replace(marker, '')

    return raw_code

def save_script_to_file(script_code: str, project_name="dogui_script"):
    directory = "C:\\Users\\sekani_b\\Desktop\\GitHub\\Projects\\IBM GEN AI\\CAU-GenAI\\cau-genai\\dev_scripts\\sekani_scripts\\autocad_automation\\scripts"
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_name}_{timestamp}.py"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w") as file:
        file.write(script_code)

    print(f"✅ DOGUI.AI-generated script saved to: {filepath}")



def call_ai_model(prompt: str, history: list = None) -> str:
    full_prompt = f"""
    You are Dogui CAD Assistant, an AI that helps engineers and students generate 2D CAD drawings using the pyautocad library.
    Your task is to take the details and information provided by the user and return the pyautocad commands needed to generate that CAD design.

    Please create the pyautocad commands needed to generate the CAD drawing using the provided description. Here is the provided description: {prompt}

    Your response should be outputted like: "Dogui: " and should not use any github markup! . Your response: 
    """
    # print("🧠 Prompt being sent to model:\n", full_prompt)
    try:
        response = model.generate_text(full_prompt)
        clean = clean_response(response)
        save_script_to_file(clean)
        return clean
    except Exception as e:
        print(f"❌ Error generating response: {e}")
        return "# AI generation failed. Please try again."


'''
Example prompt:
Based on our conversation, generate a Python script using the pyautocad library that creates the requested object(s) in AutoCAD.

Object: Square
Width: 10 feet
Height: 10 feet
Material: Wood

Please initialize AutoCAD using pyautocad, create the drawing using model space, and include comments in the code for readability.

'''


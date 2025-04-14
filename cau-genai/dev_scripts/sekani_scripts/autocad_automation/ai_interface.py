import json
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load Watson credentials from config
def load_watson_config():
    with open('config/watson_info.json') as f:
        return json.load(f)

watson_config = load_watson_config()

# Setup Watson credentials and model once
credentials = Credentials(
    url=watson_config["url"],
    api_key=watson_config["IBM_API_KEY"]
)

model = ModelInference(
    model_id=watson_config["model_id"],
    credentials=credentials,
    project_id=watson_config["project_id"]
)

# Real AI call
def call_ai_model(prompt: str) -> str:
    print("🧠 Sending prompt to IBM Watsonx AI...")
    try:
        response = model.generate_text(prompt=prompt)

        # Save prompt and response
        with open("prompts/latest_prompt.txt", "w") as f:
            f.write(prompt)
        with open("prompts/latest_response.py", "w") as f:
            f.write(response)

        return response
    except Exception as e:
        print(f"❌ Error generating response: {e}")
        return "# AI generation failed. Please try again."





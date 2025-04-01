from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

credentials = Credentials(
                   url = "https://us-south.ml.cloud.ibm.com",
                   api_key = "6JMjtZKFsxcbaokewSx68NiNLNXSmfgrx5rY_vo9HNn9"
                  )

model_id = "ibm/granite-20b-multilingual"  # Choose a model (e.g., Granite, Flan, Mistral)

# Initialize model
model = Model(
    model_id=model_id,
    credentials=credentials,
    project_id="ba1d12f8-da6f-4cb1-a8a0-47c51a1285b7"  # Found in IBM Cloud
)

# Simple request-response test
# prompt = "Hello my name is DOGUI.AI, what can you do"
prompt = "What is 2 + 2?"
response = model.generate_text(prompt)

print(response)

#print("Response:", response["results"][0]["generated_text"])

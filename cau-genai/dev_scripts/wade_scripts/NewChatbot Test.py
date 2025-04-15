from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    api_key="6JMjtZKFsxcbaokewSx68NiNLNXSmfgrx5rY_vo9HNn9"
)

model_id = "ibm/granite-vision-3-2-2b"

params = {
    "frequency_penalty": 0,
    "max_tokens": 2000,
    "presence_penalty": 0,
    "temperature": 0.7,  # Increased temperature for variety
    "top_p": 0.9         # Adjusted for a broader token selection
}

model = Model(
    model_id=model_id,
    credentials=credentials,
    params=params,
    project_id="ba1d12f8-da6f-4cb1-a8a0-47c51a1285b7"
)

prompt = "Can you provide a detailed explanation of how the human circulatory system works?"

response = model.generate_text(prompt)

# Check if the response is valid and print the full content
if 'data' in response:
    print(response['data'])
else:
    print("Response:", response)








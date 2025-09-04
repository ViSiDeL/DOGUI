from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url = "https://us-south.ml.cloud.ibm.com",
    api_key = "[SECRET]",
)

client = APIClient(credentials)

model = ModelInference(
  model_id="ibm/granite-3-8b-instruct",
  api_client=client,
  project_id="[SECRET]",
  params = {
      "max_new_tokens": 100
  }
)

prompt = 'How far is Paris from Bangalore?'
print(model.generate(prompt))
print(model.generate_text(prompt))
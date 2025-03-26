from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url = "https://us-south.ml.cloud.ibm.com",
    api_key = "cEIFOiNL-HFIHaVQFj_FwGZXFPWSZSqATF3C9hz1aGb8",
)

client = APIClient(credentials)

model = ModelInference(
  model_id="ibm/granite-3-8b-instruct",
  api_client=client,
  project_id="23c626c0-68d9-4ebc-b7aa-768776c143d0",
  params = {
      "max_new_tokens": 100
  }
)

prompt = 'How far is Paris from Bangalore?'
print(model.generate(prompt))
print(model.generate_text(prompt))
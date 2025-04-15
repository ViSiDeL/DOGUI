from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

credentials= Credentials(
                        url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29",
                        api_key="[SECRET]"
)
model_id="ibm/granite-vision-3-2-2b"



params= {
    "frequency_penalty": 0,
	"max_tokens": 2000,
	"presence_penalty": 0,
	"temperature": 0,
	"top_p": 1
    }

model= Model(
	model_id=model_id,
	credentials= credentials,
    params=params,
	project_id= "[SECRET]"

   
)



prompt= "What is 2 + 2" 
response= model.generate_text(prompt)

print(response)

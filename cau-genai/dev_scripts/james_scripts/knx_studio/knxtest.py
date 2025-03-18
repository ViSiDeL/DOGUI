from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import os
from dotenv import load_dotenv

# get credentials from .env
load_dotenv()
API_KEY = os.getenv("IBM_NLU_API_KEY")
SERVICE_URL = os.getenv("IBM_NLU_URL")
MODEL_ID = os.getenv("CUSTOM_MODEL_ID")

# set up NLU with key & url
authenticator = IAMAuthenticator(API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version="2021-08-01",
    authenticator=authenticator
)
nlu.set_service_url(SERVICE_URL)

# sending request to nlu (with custom model in entitiesoptions)
response = nlu.analyze(
    text="Apple is a company that makes decent devices in many countries",
    features=Features(entities=EntitiesOptions(model=MODEL_ID))
    # features=Features(entities=EntitiesOptions())
).get_result()

print(response)
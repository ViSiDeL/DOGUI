"""
This class handles the controller's connection to watson

"""

import os
from dotenv import load_dotenv
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class WatsonConnector:
    def __init__(self):
        load_dotenv() 
        authenticator = IAMAuthenticator(os.getenv("IBM_API_KEY"))
        self.assistant = AssistantV2(
            version='2021-06-14',
            authenticator=authenticator
        )
        self.assistant.set_service_url(os.getenv("IBM_SERVICE_URL"))
        self.assistant_id = os.getenv("IBM_ASSISTANT_ID")

    def get_response(self, user_input):
        response = self.assistant.message_stateless(
            assistant_id=self.assistant_id,
            input={'text': user_input}
        ).get_result()
        return response['output']['generic'][0]['text']

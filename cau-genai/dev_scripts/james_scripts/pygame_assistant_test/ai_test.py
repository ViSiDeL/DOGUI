# Assisted by watsonx Code Assistant 
# watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Replace with your own values
api_key = 'your_api_key'
url = 'your_service_url'

authenticator = IAMAuthenticator(api_key)
text_to_speech = TextToSpeechV1(
    version='2017-05-11',
    authenticator=authenticator
)

text_to_speech.set_service_url(url)


# Assisted by watsonx Code Assistant 
# watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
def text_to_speech_conversion(text):
    # Define the voice configuration
    voice = 'en-US_AllisonV3'  # You can choose from various voices and languages

    # Synthesize speech
    synthesis_result = text_to_speech.synthesize(
        text,
        voice=voice,
        accept='audio/wav'
    ).get_result()

    # Save the audio file
    with open('output.wav', 'wb') as f:
        f.write(synthesis_result.content)


# Assisted by watsonx Code Assistant 
# watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
text = "Hello, this is a test from IBM Watson Text-to-Speech."
text_to_speech_conversion(text)

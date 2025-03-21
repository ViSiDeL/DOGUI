'''
curl -X POST -u "apikey:{[SECRET]}" 
--header "Content-Type: audio/flac" 
--data-binary ./audio-file.flac 
"{https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/[SECRET]}/v1/recognize"
'''

from os.path import join, dirname
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('[SECRET]')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/[SECRET]')


# record
    # wait for mic input

    # process to flac


# send to cloud
with open(join(dirname(__file__), './.', 'Recording.flac'),
               'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/flac',
        word_alternatives_threshold=0.9,
        keywords=['colorado', 'tornado', 'tornadoes'],
        keywords_threshold=0.5
    ).get_result()
# print(json.dumps(speech_recognition_results, indent=2))

print(speech_recognition_results["results"][0]["alternatives"][0]["transcript"])
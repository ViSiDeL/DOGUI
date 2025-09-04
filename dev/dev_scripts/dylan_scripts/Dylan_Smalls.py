'''
curl -X POST -u "apikey:{[REMOVEDSECRET]}" 
--header "Content-Type: audio/flac" 
--data-binary ./audio-file.flac 
"{https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/[REMOVEDSECRET]}/v1/recognize"
'''

from os.path import join, dirname
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import speech_recognition as sr


authenticator = IAMAuthenticator('[REMOVEDSECRET]')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/[REMOVEDSECRET]')


recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("\nSpeak into the MIC:")
    recognizer.adjust_for_ambient_noise(source)
    audio= recognizer.listen(source)
    

    try:
        audio = recognizer.listen(source, timeout = 2, phrase_time_limit = 6)

        with open("output.wav", 'wb') as file:
            file.write(audio.get_wav_data())

        with open("output.wav", 'rb') as file:
            result = speech_to_text.recognize(
                audio=file,
                content_type='audio/wav',
                model= 'en-US_BroadbandModel'
            ).get_result()
        
        if result.get("results") and len(result["results"]) > 0:
            transcript = result['results'][0]['alternatives'][0]['transcript']
            print("Watson Transcription:", transcript, '\n')
        else:
            print("\n No speech detected.Speak louder or check your mic settings. Please try again.")

        

        # transcript = result['results'][0]['alternatives'][0]['transcript']
        # print("Watson Transcription:", transcript,'\n')

    except sr.WaitTimeoutError:
        print("\n No speech detected.Speak louder or check your mic settings. Please try again.")

    # while audio != None:
    #     audio = recognizer.listen(source)
 


# with open("output.wav", 'wb') as file:
#     file.write(audio.get_wav_data())

# with open("output.wav", 'rb') as file:
#     result = speech_to_text.recognize(
#         audio=file,
#         content_type='audio/wav',
#         model= 'en-US_BroadbandModel'
#     ).get_result()

# transcript = result['results'][0]['alternatives'][0]['transcript']
# print("Watson Transcription:", transcript,'\n')




# # send to cloud
# with open(join(dirname(__file__), './.', 'Recording.flac'),
#                'rb') as audio_file:
#     speech_recognition_results = speech_to_text.recognize(
#         audio=audio_file,
#         content_type='audio/flac',
#         word_alternatives_threshold=0.9,
#         keywords=['colorado', 'tornado', 'tornadoes'],
#         keywords_threshold=0.5
#     ).get_result()
# # print(json.dumps(speech_recognition_results, indent=2))

# print(speech_recognition_results["results"][0]["alternatives"][0]["transcript"])
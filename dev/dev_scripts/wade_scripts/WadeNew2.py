from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

languages = {
    "English": "en-US_MichaelV3Voice",
    "Japanese": "ja-JP_EmiV3Voice",
    "Arabic": "ar-AR_OmarV3Voice",
    "Spanish":"es-ES_EnriqueV3Voice",
    "French":"fr-FR_ReneeV3Voice",
    "Dutch":"nl-NL_MerelV3Voice",
    "German": "de-DE_DieterV3Voice",
    "Italian": "it-IT_FrancescaV3Voice",
    "Korean": "ko-KR_JinV3Voice",
    "Portuguese": "pt-BR_IsabelaV3Voice",
    "Castillain Spanish":"es-ES_EnriqueV3Voice",
    "Latin Spanish":"es-LA_SoftiaV3Voice",
    "French Canadian":"fr-CA_LouiseV3Voice",
    
}

# Function to synthesize text-to-speech with dynamic input
def synthesize_speech(text, voice, output_file):
    # Set up the authenticator
    authenticator = IAMAuthenticator('[REMOVEDSECRET]')
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    # Set the service URL
    text_to_speech.set_service_url('https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/[REMOVEDSECRET]')

    # Synthesize the speech from text
    with open(output_file, 'wb') as audio_file:
        response = text_to_speech.synthesize(
            text,
            voice=voice,
            accept='audio/wav'
        ).get_result()
        
        # Write the audio response to a file
        audio_file.write(response.content)
        print(f"Speech saved to {output_file}")

# Input your text and choose the voice
text_input = input("Enter the text you want to convert to speech: ")
voice_choice = input("Enter the voice language (e.g., en-US_MichaelV3Voice , ja-JP_EmiV3Voice , ar-AR_OmarV3Voice,fr-FR_ReneeV3Voice,es-ES_EnriqueV3Voice,nl-NL_MerelV3Voice,de-DE_DieterV3Voic,it-IT_FrancescaV3Voice,ko-KR_JinV3Voice,pt-BR_IsabelaV3Voice,es-ES_EnriqueV3Voice,es-LA_SoftiaV3Voice,fr-CA_LouiseV3Voice")
voice_choice = voice_choice.capitalize()
converted_voice_choice = languages[voice_choice]
output_filename = 'output_audio.wav'

# Call the function to synthesize speech
synthesize_speech(text_input, converted_voice_choice, output_filename)

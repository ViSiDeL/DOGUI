from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

languages = {
    "English": "en-US_MichaelV3Voice",
    "Japanese": "ja-JP_EmiV3Voice",
    "Arabic": "ar-AR_OmarV3Voice"
}

# Function to synthesize text-to-speech with dynamic input
def synthesize_speech(text, voice, output_file):
    # Set up the authenticator
    authenticator = IAMAuthenticator('KqT8Q6GzdQPN21zuzysaJLhF6Yb6MWLYXD4c5F5Xuxwd')
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    # Set the service URL
    text_to_speech.set_service_url('https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/be845ad2-9c3d-4b57-a046-f3b8f6f3bda2')

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
voice_choice = input("Enter the voice language (e.g., en-US_MichaelV3Voice , ja-JP_EmiV3Voice , ar-AR_OmarV3Voice): ")
voice_choice = voice_choice.capitalize()
converted_voice_choice = languages[voice_choice]
output_filename = 'output_audio.wav'

# Call the function to synthesize speech
synthesize_speech(text_input, converted_voice_choice, output_filename)

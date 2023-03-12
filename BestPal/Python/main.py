# The above command writes the programme to a file called main.py

# Import namespaces
from dotenv import load_dotenv
from datetime import datetime
import os
import openai
import time
import azure.cognitiveservices.speech as speech_sdk

# Get Configuration Settings
load_dotenv()
cog_key = os.getenv('COG_SERVICE_KEY')
cog_region = os.getenv('COG_SERVICE_REGION')
openai_key = os.getenv('OPENAI_API_KEY')

# Configure speech service
speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)

# Configure speech synthesis
speech_config.speech_synthesis_voice_name = "en-GB-LibbyNeural"
speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

# Configure openai
openai.api_key = openai_key

# Function to transcribe speech to text
def transcribe_command():
    command = ''

    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now... (say quit to exit)')

     # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command

# Function to call openai 
def call_openai(command):

    # Query openai
    # Adjust temperature, max_tokens, top_p, frequency_penalty, presence_penalty
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=command,
        temperature=0.9,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    # Print and read aloud answer from openai
    answer = response['choices'][0]['text']
    return answer

# Function to read aloud text
def read_aloud(read_aloud_text):
    # Print the response
    print(read_aloud_text)

    # Abbi,Alfie,Bella,Elliot,Ethan,Hollie,Libby,Maisie,Noah,Oliver,Olivia,Ryan,Sonia,Thomas
    voice = "en-GB-LibbyNeural"
    
    # Synthesize spoken output
    responseSsml = " \
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
            <voice name='{}'> \
                {} \
            </voice> \
        </speak>".format(voice, read_aloud_text)
    speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
  
# Main function
def main():
    while True:
        try:           
            # Get spoken input
            command = transcribe_command()

            # Handle no input
            if command.lower() == '':
                time.sleep(3)
                print('Waiting 2 seconds...')
                continue
            
            # Handle quit
            elif command.lower() == 'quit.':
                break   
            
            # Handle time case (specific phrase)
            elif command.lower() == 'what time is it?':
                now = datetime.now()
                read_aloud_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)
                read_aloud(read_aloud_text)

            # Handle general case 
            else:
                answer = call_openai(command.lower())
                read_aloud(answer)

        except Exception as ex:
            print(ex)

# Run the main function
if __name__ == "__main__":
    main()

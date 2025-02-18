# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
#from be.settings import OPENAI_API_KEY
from pydub import AudioSegment

import io
import ffmpeg
import tempfile
import os




class AudioTranscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept WebSocket connection
        self.room_name = "audio_transcription"
        self.room_group_name = f"audio_{self.room_name}"

        await self.accept()

    async def receive(self, bytes_data):
        # If the message is binary (audio data), process it
        if isinstance(bytes_data, bytes):
            audio_data = bytes_data

            # Transcribe audio data
            self.transcribe_audio(audio_data)

    async def transcribe_audio(self, audio_data):
        try:

             # Save accumulated audio to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_audio_file:
                temp_audio_file.write(audio_data)
                temp_audio_file_path = temp_audio_file.name
            """
            client = OpenAI(api_key=OPENAI_API_KEY)
            with open(temp_audio_file.name, 'rb') as f:
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f,  
                        language="cs"
                )
            print(response.text)  
            """  
            
            # Convert the temporary file to a format readable by pydub

            # Clean up the temporary file
            os.remove(temp_audio_file_path)
            """
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
            client = OpenAI(api_key=OPENAI_API_KEY)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav_file:
            # Export audio to the temporary file in WAV format
                audio.export(temp_wav_file, format="wav")
                temp_wav_file.close()  # Close the file so it can be used by OpenAI API

                #print(f"Converted audio to WAV, saved at {temp_wav_file.name}")
                # OpenAI API call using the temporary WAV file
                print("Transcribing audio...")          
                with open(temp_wav_file.name, 'rb') as f:
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f,  # Send the actual file object to OpenAI API
                        language="cs"
                )
            """

            #print(response.text)
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return "Error during transcription."

    async def disconnect(self, close_code):
        # Handle disconnection if needed
        pass

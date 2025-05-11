"""
================================================================================
 Module: consumersSurvey.py
 Description: 
        Implements an asynchronous WebSocket consumer that handles real-time audio 
        streaming from the client where user answers survey questions, sends it speech-to-text service and saves transcription,
 Author: Dominik Horut (xhorut01)
================================================================================
"""

import asyncio
import azure.cognitiveservices.speech as speechsdk
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime
from be.settings import AZURE_API_KEY, AZURE_REGION
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")
django.setup()
from .utils import get_skill_names_string

SURVEY_DIR = "survey"
os.makedirs(SURVEY_DIR, exist_ok=True)

class SurveySpeechTranscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Buffer for incoming audio data
        self.speech_data = bytearray()

        self.full_transcript = ""

        # Survey question data
        self.question_text = ""
        self.skills = []
        self.skill_names = ""

        self.loop = asyncio.get_event_loop()
        self.executor = asyncio.get_running_loop().run_in_executor
        self.language = "cs-CZ"
        
        self.speech_recognizer, self.stream = self.create_speech_recognizer()
        
        await self.accept()
        print("WebSocket connection established")

    async def disconnect(self, close_code):

        # User terminated question answering - save the transcription 
        self.stream.close()
        self.speech_recognizer.stop_continuous_recognition()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        json_filename = f"voice_{timestamp}.json"

        json_filepath = os.path.join(SURVEY_DIR, json_filename)
        
        survey_question_data = {
            "question_text": self.question_text,
            "answer": self.full_transcript,
            "examples_type": self.skill_names,
            "timestamp": timestamp
        }

        with open(json_filepath, "w", encoding="utf-8") as json_file:
            json.dump(survey_question_data, json_file, indent=4, ensure_ascii=False)
        
    async def receive(self, text_data=None, bytes_data=None):

        # Metadata was received via websocket
        if text_data:
            try:
                # Parse the metadata sent from the client
                metadata = json.loads(text_data)
                self.question_text = metadata.get("question_text")
                self.skills = metadata.get("skills")
                self.skill_names = await get_skill_names_string(self.skills)

                # Check if language was changed
                if 'language' in metadata:
                    self.language = metadata['language']
                    self.speech_recognizer.stop_continuous_recognition()
                    self.speech_recognizer, self.stream = self.create_speech_recognizer()

            except json.JSONDecodeError:
                print("Invalid metadata received")

        # Audio data was received via websocket
        elif bytes_data:
            self.stream.write(bytes_data)

    def create_speech_recognizer(self):

        # Azure STT configuration   
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        audio_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=1)
        stream = speechsdk.audio.PushAudioInputStream(stream_format=audio_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
            language=self.language  
        )
        
        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            if evt.result.text:

                self.full_transcript += evt.result.text + " "
                
                asyncio.run_coroutine_threadsafe(
                    self.send(json.dumps({"transcription": evt.result.text})),
                    self.loop
                )            
        
        speech_recognizer.recognized.connect(recognized_cb)
        
        speech_recognizer.start_continuous_recognition_async()
        
        return speech_recognizer, stream
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

SURVEY_DIR = "survey"
os.makedirs(SURVEY_DIR, exist_ok=True)


class SurveySpeechTranscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.speech_data = bytearray()
        self.full_transcript = ""
        self.question_text = ""
        self.loop = asyncio.get_event_loop()
        self.executor = asyncio.get_running_loop().run_in_executor
        
        self.speech_recognizer, self.stream = self.create_speech_recognizer()
        
        await self.accept()
        print("WebSocket connection established")

    async def disconnect(self, close_code):
        self.stream.close()
        self.speech_recognizer.stop_continuous_recognition()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        json_filename = f"voice_{timestamp}.json"

        json_filepath = os.path.join(SURVEY_DIR, json_filename)
        
        print(self.full_transcript)

        survey_question_data = {
            "question_text": self.question_text,
            "answer": self.full_transcript,
            "timestamp": timestamp
        }

        with open(json_filepath, "w", encoding="utf-8") as json_file:
            json.dump(survey_question_data, json_file, indent=4, ensure_ascii=False)
        
        print(f"WebSocket connection closed with code: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                metadata = json.loads(text_data)
                self.question_text = metadata.get("question_text")
                print(metadata.get("question_text"))    
            except json.JSONDecodeError:
                print("Invalid metadata received")
        
        elif bytes_data:
            self.stream.write(bytes_data)

    def create_speech_recognizer(self):
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        
        audio_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=1)
        stream = speechsdk.audio.PushAudioInputStream(stream_format=audio_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
            language="cs-CZ"  
        )
        
        # Set up event handlers
        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            if evt.result.text:

                self.full_transcript += evt.result.text + " "
                
                asyncio.run_coroutine_threadsafe(
                    self.send(json.dumps({"transcription": evt.result.text})),
                    self.loop
                )            
        
        # Connect event handlers
        speech_recognizer.recognized.connect(recognized_cb)
        
        # Start continuous recognition
        speech_recognizer.start_continuous_recognition_async()
        
        return speech_recognizer, stream
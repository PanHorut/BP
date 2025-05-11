"""
================================================================================
 Module: consumers.py
 Description: 
        Implements an asynchronous WebSocket consumer that handles real-time audio 
        streaming from the client where user answers example answers, sends it speech-to-text service and gets transcription,
        evaluates the transcribed answer and sends result back to client. 
 Author: Dominik Horut (xhorut01)
================================================================================
"""

import asyncio
import azure.cognitiveservices.speech as speechsdk
from channels.generic.websocket import AsyncWebsocketConsumer
from be.settings import AZURE_API_KEY, AZURE_REGION
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor
import json
import django
import io
import wave
from django.test import RequestFactory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")
django.setup()

from .views import skip_example, delete_example_record
from .answerChecker import GeminiRateLimitError

AUDIO_DIR = "audioprompts"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Set to True to enable audio dumping
DUMP_AUDIO=False

class SpeechRecognitionConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Buffer for incoming audio data
        self.speech_data = bytearray()

        self.message_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.language = "cs-CZ"
        
        # Metadata about language, user and currently solved example
        self.metadata = {}
        self.audio_format = None

        # Set up Azure speech recognizer and audio stream
        self.speech_recognizer, self.stream = self.create_speech_recognizer()
        
        await self.accept()
        
        # Start receiving audio
        asyncio.create_task(self.receive_audio())

    async def disconnect(self, close_code):
        self.stream.close()
        self.speech_recognizer.stop_continuous_recognition()
        self.executor.shutdown(wait=False)
        print("Speech recognition stopped.")

    async def receive(self, text_data=None, bytes_data=None):

        # Metadata was received via websocket
        if text_data:
            try:
                new_metadata = json.loads(text_data)
                self.metadata.update(new_metadata)
            
                if 'format' in new_metadata:
                    self.audio_format = new_metadata['format']
                
                # Check if language was changed
                if 'language' in new_metadata:
                    self.language = new_metadata['language']
                    print(f"Language changed to: {self.language}")
                    self.speech_recognizer.stop_continuous_recognition()
                    self.speech_recognizer, self.stream = self.create_speech_recognizer()
                
            except json.JSONDecodeError:
                print("Invalid metadata received.")

        # Audio data was received via websocket
        elif bytes_data:
            # Send raw PCM data directly to Azure
            self.stream.write(bytes_data)
            
            # Accumulate audio data to dump
            self.speech_data.extend(bytes_data)

    async def receive_audio(self):
        while True:
            await asyncio.sleep(0.1)

    def create_speech_recognizer(self):

        # Azure STT configuration   
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=1)
        stream = speechsdk.audio.PushAudioInputStream(stream_format=format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
            language=self.language
        )

        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            if evt.result.text and self.speech_data:
                
                student_id = self.metadata.get('student_id', 'unknown')
                example_id = self.metadata.get('example_id', 'unknown')

                # Sent audio will be dumped in WAV
                if DUMP_AUDIO:  
                   
                    wav_data = self.convert_pcm_to_wav(self.speech_data)
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

                    audio_filename = f"{student_id}_{example_id}_{timestamp}.wav"
                    json_filename = f"{student_id}_{example_id}_{timestamp}.json"

                    audio_filepath = os.path.join(AUDIO_DIR, audio_filename)
                    json_filepath = os.path.join(AUDIO_DIR, json_filename)

                    with open(audio_filepath, "wb") as f:
                        f.write(wav_data)
        
                from .models import Example, Answer

                # Get example text and correct answer
                try:
                    example = Example.objects.get(id=example_id)
                    answer = Answer.objects.filter(example=example).first() 
                    correct_answer = answer.answer if answer else "No correct answer found"
                except Example.DoesNotExist:
                    example_text = "Example not found"
                    correct_answer = "No correct answer found"
                else:
                    example_text = example.example

                # Reset accumulated audio data
                self.speech_data = bytearray()
                
                from .utils import calculate_duration
                from .answerChecker import InlineSpeechAnswerChecker, FractionSpeechAnswerChecker, VariableSpeechAnswerChecker, LLMAnswerChecker

                # Get data for current example
                input_type = self.metadata.get('input_type')
                record_date = self.metadata.get('record_date')
                duration = calculate_duration(record_date)
                student_answer = evt.result.text

                # Words to skip example or terminate practice
                skip_wordsCS = ["přeskočit", "další", "přeskoč", "dál"]
                skip_wordsEN = ["skip", "next", "continue"]
                finish_wordsCS = ["konec", "ukončit", "stačí", "hotovo", "skončit", "dost"]
                finish_wordsEN = ["finish", "end", "stop", "done"]

                if(self.language == "cs-CZ"):
                    skip_words = skip_wordsCS
                    finish_words = finish_wordsCS
                else:
                    skip_words = skip_wordsEN
                    finish_words = finish_wordsEN

                # Transcript containts 'skip' words - update record and skip example
                if any(word in student_answer.lower() for word in skip_words):
                    factory = RequestFactory()
                    request = factory.post('skip-example/', {
                        'student_id': student_id,
                        'example_id': example_id,
                        'date': record_date
                    })
                    skip_example(request)
                    response_data = {'skipped': True}
                    evaluation_data = {
                        "student_id": student_id,
                        "example_id": example_id,
                        "transcription": evt.result.text,
                        "example_text": example_text,
                        "correct_answer": correct_answer,
                        "evaluation": "skipped"
                    }

                # Transcript containts 'terminate' words - delete record and terminate practice
                elif any(word in student_answer.lower() for word in finish_words):
                    factory = RequestFactory()
                    request = factory.post('delete-record/', {
                        'student_id': student_id,
                        'example_id': example_id,
                        'date': record_date
                    })
                    delete_example_record(request)
                    response_data = {'finished': True}
                    evaluation_data = {
                        "student_id": student_id,
                        "example_id": example_id,
                        "transcription": evt.result.text,
                        "example_text": example_text,
                        "correct_answer": correct_answer,
                        "evaluation": "terminated"
                    }

                # Transcript does not contain 'skip' or 'terminate' words - evaluate answer 
                else:
                    # Basic answer formats evaluated by script
                    if input_type == 'INLINE' or input_type == 'WORD':
                        isCorrect, continue_with_next, student_answer = InlineSpeechAnswerChecker.verifyAnswer(
                            student_id, example_id, record_date, duration, student_answer
                        )
                    # Fraction answer evaluated by LLM
                    elif input_type == 'FRAC':
                        
                        try:
                            isCorrect, continue_with_next, student_answer = LLMAnswerChecker.verifyAnswer(
                                student_id, example_id, record_date, duration, student_answer, 'fraction'
                            )

                        # LLM rate limit reached - use FractionSpeechAnswerChecker
                        except GeminiRateLimitError:
                            print("FRAC gemini limit reached - will use FractionSpeechAnswerChecker")
                            isCorrect, continue_with_next, student_answer = FractionSpeechAnswerChecker.verifyAnswer(
                                student_id, example_id, record_date, duration, student_answer
                            )                               

                    # Variable answer evaluated by LLM  
                    elif input_type == 'VAR':

                        try:
                            isCorrect, continue_with_next, student_answer = LLMAnswerChecker.verifyAnswer(
                                student_id, example_id, record_date, duration, student_answer, 'variable'
                            )

                        # LLM rate limit reached - use VariableSpeechAnswerChecker
                        except GeminiRateLimitError:
                            print("VAR gemini limit reached - will use VariableSpeechAnswerChecker")
                            isCorrect, continue_with_next, student_answer = VariableSpeechAnswerChecker.verifyAnswer(
                            student_id, example_id, record_date, duration, student_answer
                        )
                    
                    # Return evaluation result back to client
                    response_data = {
                        "isCorrect": isCorrect,
                        "continue_with_next": continue_with_next,
                        "student_answer": student_answer
                    }

                    # Advanced evaluation data to be dumped in JSON
                    evaluation_data = {
                        "student_id": student_id,
                        "example_id": example_id,
                        "transcription": evt.result.text,
                        "example_text": example_text,
                        "correct_answer": correct_answer,
                        "evaluation": isCorrect
                    }

                # Save evaluation data to JSON file
                if DUMP_AUDIO:
                    with open(json_filepath, "w", encoding="utf-8") as json_file:
                        json.dump(evaluation_data, json_file, indent=4, ensure_ascii=False)

                    print(f"Evaluation saved: {json_filepath}")

                asyncio.run_coroutine_threadsafe(
                    self.send(json.dumps(response_data)),
                    self.loop
                )
                
        def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            try:
                if evt.result.text:
                    future = asyncio.run_coroutine_threadsafe(
                        self.message_queue.put(f"[interim] {evt.result.text}"),
                        self.loop
                    )
                    future.result() 
            except Exception as e:
                print(f"Error in recognizing callback: {e}")

        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.recognizing.connect(recognizing_cb)

        # Starts recognition in a separate thread to avoid blocking
        def start_recognition():
            speech_recognizer.start_continuous_recognition()

        self.executor.submit(start_recognition)
        
        return speech_recognizer, stream
        
    def convert_pcm_to_wav(self, pcm_data):
        # Converts raw PCM data sent from client to WAV format
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, 'wb') as wav_file:
                wav_file.setnchannels(1)        # Mono
                wav_file.setsampwidth(2)        # 16-bit
                wav_file.setframerate(16000)    # 16kHz
                wav_file.writeframes(pcm_data)
            return wav_io.getvalue()
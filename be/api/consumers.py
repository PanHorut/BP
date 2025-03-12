import asyncio
import azure.cognitiveservices.speech as speechsdk
from channels.generic.websocket import AsyncWebsocketConsumer

from be.settings import AZURE_API_KEY, AZURE_REGION

from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor
import json
import tempfile
import subprocess
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")
django.setup()

from django.test import RequestFactory
from .views import skip_example, delete_example_record
from .models import AudioPrompt, Student, Example



class SpeechRecognitionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.speech_data = b""  # Accumulate audio for each segment
        self.message_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.webm_header = None  # Store WebM header for reuse
        self.is_first_chunk = True  # Track if this is the first chunk

        self.metadata = {}

        # Create Azure Speech recognizer and stream
        self.speech_recognizer, self.stream = self.create_speech_recognizer()
        
        # Accept WebSocket connection
        await self.accept()
        
        # Start receiving audio
        asyncio.create_task(self.receive_audio())

    async def disconnect(self, close_code):
        self.stream.close()
        self.speech_recognizer.stop_continuous_recognition()
        self.executor.shutdown(wait=False)
        print("Speech recognition stopped.")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                new_metadata = json.loads(text_data)
                self.metadata.update(new_metadata)  
            except json.JSONDecodeError:
                print("Invalid metadata received.")
        elif bytes_data:
            # If this is the first chunk ever received, store the WebM header
            if self.is_first_chunk:

                self.webm_header = bytes_data
                self.is_first_chunk = False
                print("Stored WebM header from first chunk")
            
            # Send to Azure for processing
            self.stream.write(bytes_data)
            
            # Accumulate audio for the current segment
            self.speech_data += bytes_data

    async def receive_audio(self):
        while True:
            await asyncio.sleep(0.1)

    def create_speech_recognizer(self):
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        format = speechsdk.audio.AudioStreamFormat(compressed_stream_format=speechsdk.AudioStreamContainerFormat.ANY)
        stream = speechsdk.audio.PushAudioInputStream(format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
            language="cs-CZ"
        )

        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            if evt.result.text and self.speech_data: 

                current_audio_data = self.speech_data
        
                self.speech_data = b""

                if self.webm_header is not None:
                    header_size = min(4096, len(self.webm_header))  # first 4KB or less as header
                    webm_header = self.webm_header[:header_size]
            
                    

                    if not current_audio_data.startswith(webm_header[:20]):
                        final_audio_data = webm_header + current_audio_data
                    else:
                        final_audio_data = current_audio_data
                else:
                    final_audio_data = current_audio_data
                
                student_id = self.metadata.get('student_id')
                example_id = self.metadata.get('example_id')

                student = None
                example = None
                
                if student_id:
                    try:
                        student = Student.objects.get(id=student_id)
                    except Student.DoesNotExist:
                        print(f"Student with ID {student_id} not found")

                if example_id:
                    try:
                        example = Example.objects.get(id=example_id)
                    except Example.DoesNotExist:
                        print(f"Example with ID {example_id} not found")
                    
                recording = AudioPrompt(
                        audio_data=final_audio_data,
                        transcription=evt.result.text,
                        student=student,
                        example=example
                    )
                recording.save()
                from .utils import calculate_duration
                from .answerChecker import InlineSpeechAnswerChecker, FractionSpeechAnswerChecker, VariableSpeechAnswerChecker

                student_id = self.metadata.get('student_id')
                example_id = self.metadata.get('example_id')
                input_type = self.metadata.get('input_type')
                record_date = self.metadata.get('record_date')

                duration = calculate_duration(record_date)
                student_answer = evt.result.text

                skip_words = ["nevím", "netuším", "přeskočit", "další", "přeskoč"]
                finish_words = ["konec", "ukončit", "stačí", "hotovo", "skončit", "dost"]

                if any(word in student_answer.lower() for word in skip_words):
                    factory = RequestFactory()
                    request = factory.post('skip-example/', {
                        'student_id': student_id,
                        'example_id': example_id,
                        'date': record_date
                    })
                    skip_example(request)
                    response_data = {'skipped': True}

                elif any(word in student_answer.lower() for word in finish_words):
                    factory = RequestFactory()
                    request = factory.post('delete-record/', {
                        'student_id': student_id,
                        'example_id': example_id,
                        'date': record_date
                    })
                    delete_example_record(request)
                    response_data = {'finished': True}

                else:
                    if input_type == 'INLINE':
                        isCorrect, continue_with_next, student_answer = InlineSpeechAnswerChecker.verifyAnswer(
                            student_id, example_id, record_date, duration, student_answer
                        )

                    elif input_type == 'FRAC':
                        isCorrect, continue_with_next, student_answer = FractionSpeechAnswerChecker.verifyAnswer(
                            student_id, example_id, record_date, duration, student_answer
                        )

                    elif input_type == 'VAR':
                        isCorrect, continue_with_next, student_answer = VariableSpeechAnswerChecker.verifyAnswer(
                            student_id, example_id, record_date, duration, student_answer
                        )

                    response_data = {
                        "isCorrect": isCorrect,
                        "continue_with_next": continue_with_next,
                        "student_answer": student_answer
                    }

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
                    future.result()  # Ensure processing
            except Exception as e:
                print(f"Error in recognizing callback: {e}")

        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.recognizing.connect(recognizing_cb)

        # Start recognition in a separate thread to avoid blocking
        def start_recognition():
            speech_recognizer.start_continuous_recognition()

        self.executor.submit(start_recognition)
        
        return speech_recognizer, stream
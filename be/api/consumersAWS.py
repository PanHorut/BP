import asyncio
import json
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import django
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from channels.generic.websocket import AsyncWebsocketConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")
django.setup()

from django.test import RequestFactory
from .views import skip_example, delete_example_record
from .models import AudioPrompt, Student, Example


# AWS Configuration
REGION = "eu-central-1"  # Update this to your AWS region
SAMPLE_RATE = 16000  # Update based on your audio settings


class TranscribeEventHandler(TranscriptResultStreamHandler):
    def __init__(self, stream_client, consumer):
        super().__init__(stream_client)
        self.consumer = consumer
        self.transcribed_text = ""
        self.final_transcript = ""

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        print(results)
    
        for result in results:
            print(f"Received result: {result}")
            
            # Handle interim results (not final)
            if result.is_partial:
                for alt in result.alternatives:
                    self.transcribed_text = alt.transcript
                    print(f"Interim transcript: {self.transcribed_text}")
                    await self.consumer.send(json.dumps({"interim": self.transcribed_text}))
            
            # Handle final results
            else:
                for alt in result.alternatives:
                    self.final_transcript = alt.transcript
                    print(f"Final transcript: {self.final_transcript}")
                    await self.process_final_transcript(self.final_transcript)

    async def process_final_transcript(self, transcript):
        print(f"Processing final transcript: {transcript}")
        
        # Process the final transcript similar to Azure's recognized_cb
        if transcript and self.consumer.speech_data:
            current_audio_data = self.consumer.speech_data
            self.consumer.speech_data = b""
            
            if self.consumer.webm_header is not None:
                header_size = min(4096, len(self.consumer.webm_header))
                webm_header = self.consumer.webm_header[:header_size]
                
                if not current_audio_data.startswith(webm_header[:20]):
                    final_audio_data = webm_header + current_audio_data
                else:
                    final_audio_data = current_audio_data
            else:
                final_audio_data = current_audio_data
            
            student_id = self.consumer.metadata.get('student_id')
            example_id = self.consumer.metadata.get('example_id')
            
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
            
            # Save the audio recording
            recording = AudioPrompt(
                audio_data=final_audio_data,
                transcription=transcript,
                student=student,
                example=example
            )
            recording.save()
            from .utils import calculate_duration
            from .answerChecker import InlineSpeechAnswerChecker, FractionSpeechAnswerChecker, VariableSpeechAnswerChecker, LLMAnswerChecker
            # Process the answer
            input_type = self.consumer.metadata.get('input_type')
            record_date = self.consumer.metadata.get('record_date')
            duration = calculate_duration(record_date)
            student_answer = transcript
            
            skip_words = ["nevím", "netuším", "přeskočit", "další", "přeskoč"]
            finish_words = ["konec", "ukončit", "stačí", "hotovo", "skončit", "dost"]
            
            # Handle skip command
            if any(word in student_answer.lower() for word in skip_words):
                factory = RequestFactory()
                request = factory.post('skip-example/', {
                    'student_id': student_id,
                    'example_id': example_id,
                    'date': record_date
                })
                skip_example(request)
                response_data = {'skipped': True}
            
            # Handle finish command
            elif any(word in student_answer.lower() for word in finish_words):
                factory = RequestFactory()
                request = factory.post('delete-record/', {
                    'student_id': student_id,
                    'example_id': example_id,
                    'date': record_date
                })
                delete_example_record(request)
                response_data = {'finished': True}
            
            # Process answer with LLM checker
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
            
            print(f"Response data: {response_data}")
            await self.consumer.send(json.dumps(response_data))



class SpeechRecognitionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected.")
        self.speech_data = b""  # Accumulate audio for each segment
        self.message_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.webm_header = None  # Store WebM header for reuse
        self.is_first_chunk = True  # Track if this is the first chunk
        
        self.metadata = {}
        self.streaming_client = None
        self.transcribe_handler = None
        self.stream_task = None
        
        # Accept WebSocket connection
        await self.accept()
        print("WebSocket connection accepted.")
        
        # Start the AWS Transcribe client
        self.streaming_client = TranscribeStreamingClient(region=REGION)
        
        # Start receiving audio
        asyncio.create_task(self.receive_audio())

    async def disconnect(self, close_code):
        print("WebSocket disconnected. Closing stream and cleaning up.")
        if self.stream_task:
            self.stream_task.cancel()
            try:
                await asyncio.wait_for(self.stream_task, timeout=1.0)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                print("Stream task cancelled.")
    
        self.streaming_client = None
        self.executor.shutdown(wait=False)
        print("Speech recognition stopped.")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                new_metadata = json.loads(text_data)
                self.metadata.update(new_metadata)
                print(f"Received metadata: {new_metadata}")
                
                # If this is the first metadata received, start the stream
                if not self.stream_task and 'student_id' in self.metadata:
                    print("Starting transcription stream.")
                    self.stream_task = asyncio.create_task(self.start_transcription_stream())
            except json.JSONDecodeError:
                print("Invalid metadata received.")
        elif bytes_data:
            
            # If this is the first chunk ever received, store the WebM header
            if self.is_first_chunk:
                self.webm_header = bytes_data
                self.is_first_chunk = False
                print("Stored WebM header from first chunk")
            
            # Accumulate audio for the current segment
            self.speech_data += bytes_data
            
            # If we have a stream active, send the audio
            if hasattr(self, 'input_stream') and self.input_stream:
                try:
                    # Convert WebM to PCM if needed
                    await self.input_stream.send_audio_event(audio_chunk=bytes_data)
                except Exception as e:
                    print(f"Error sending audio to AWS Transcribe: {e}")
                    await self.send(json.dumps({"error": str(e)}))

    async def receive_audio(self):
        while True:
            await asyncio.sleep(0.1)

    async def start_transcription_stream(self):
        """Start the AWS Transcribe streaming session"""
        try:
            print("Starting transcription stream...")
            stream = await self.streaming_client.start_stream_transcription(
                language_code="cs-CZ", 
                media_sample_rate_hz=SAMPLE_RATE,
                media_encoding="ogg-opus",  
            )
            
            self.input_stream = stream.input_stream
            self.transcribe_handler = TranscribeEventHandler(stream.output_stream, self)
            
            # Start the handler in a separate task
            handler_task = asyncio.create_task(self.transcribe_handler.handle_events())
            
            # Wait for the handler to complete
            await handler_task
            
        except Exception as e:
            print(f"Error in AWS Transcribe streaming: {e}")
            await self.send(json.dumps({"error": str(e)}))

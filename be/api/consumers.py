import asyncio
import azure.cognitiveservices.speech as speechsdk
from channels.generic.websocket import AsyncWebsocketConsumer
from be.settings import AZURE_API_KEY, AZURE_REGION

from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor
import json

class SpeechRecognitionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.speech_data = b""
        self.message_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=1)

        self.metadata = {}

        
        # Create the Azure speech recognizer and audio stream
        self.speech_recognizer, self.stream = self.create_speech_recognizer()
        
        # Accept the WebSocket connection
        await self.accept()
        
        # Start receiving audio and sending recognition results
        asyncio.create_task(self.receive_audio())
    
    async def disconnect(self, close_code):
        self.stream.close()
        self.speech_recognizer.stop_continuous_recognition()
        self.executor.shutdown(wait=False)
        print("Speech recognition stopped.")
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            # Handle metadata (e.g., student_id, example_id, etc.)
            try:
                new_metadata = json.loads(text_data)
                # Update metadata dynamically
                self.metadata.update(new_metadata)
            except json.JSONDecodeError:
                print("Invalid metadata received.")
                
        elif bytes_data:
            # Write the audio data to the stream
            self.stream.write(bytes_data)
    
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
            try:
                if evt.result.text:
                    #print(f"Recognized: {evt.result.text}")
                    future = asyncio.run_coroutine_threadsafe(
                        self.message_queue.put(evt.result.text),
                        self.loop
                    )
                    future.result()  # Wait for the result to ensure it's processed

                    from .utils import calculate_duration
                    from .answerChecker import InlineSpeechAnswerChecker, FractionSpeechAnswerChecker, VariableSpeechAnswerChecker

                    student_id = self.metadata.get('student_id')
                    example_id = self.metadata.get('example_id')
                    input_type = self.metadata.get('input_type')
                    record_date = self.metadata.get('record_date')

                    duration = calculate_duration(record_date)
                    student_answer = evt.result.text

                    if(input_type == 'INLINE'):
                        isCorrect, continue_with_next = InlineSpeechAnswerChecker.verifyAnswer(student_id, example_id, record_date, duration, student_answer)

                    elif(input_type == 'FRAC'):
                        isCorrect, continue_with_next = FractionSpeechAnswerChecker.verifyAnswer(student_id, example_id, record_date, duration, student_answer)
                        
                    elif(input_type == 'VAR'):
                        isCorrect, continue_with_next = VariableSpeechAnswerChecker.verifyAnswer(student_id, example_id, record_date, duration, student_answer)


                    response_data = {
                        "isCorrect": isCorrect,
                        "continue_with_next": continue_with_next
                    }

                    asyncio.run_coroutine_threadsafe(
                        self.send(json.dumps(response_data)),
                        self.loop
                    )
                    

            except Exception as e:
                print(f"Error in recognized callback: {e}")

        def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            try:
                if evt.result.text:
                    #print(f"Recognizing: {evt.result.text}")
                    future = asyncio.run_coroutine_threadsafe(
                        self.message_queue.put(f"[interim] {evt.result.text}"),
                        self.loop
                    )
                    future.result()  # Wait for the result to ensure it's processed
            except Exception as e:
                print(f"Error in recognizing callback: {e}")

        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.recognizing.connect(recognizing_cb)
        
        # Start recognition in a separate thread to avoid blocking
        def start_recognition():
            speech_recognizer.start_continuous_recognition()
        
            
        self.executor.submit(start_recognition)
        
        return speech_recognizer, stream
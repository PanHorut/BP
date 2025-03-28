import asyncio
import pyaudio
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

SAMPLE_RATE = 16000
BYTES_PER_SAMPLE = 2
CHANNEL_NUMS = 1
CHUNK_SIZE = 1024  # Reduced chunk size for faster processing
REGION = "eu-central-1"  # Region as specified

class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        # Process transcriptions as they come in
        results = transcript_event.transcript.results
        for result in results:
            if not result.is_partial:  # Only handle final results
                for alt in result.alternatives:
                    print(f"💬 Transcription: {alt.transcript}")

async def mic_stream():
    """Capture microphone audio in chunks for real-time processing."""
    p = pyaudio.PyAudio()

    # Open the microphone stream with lower chunk size
    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNEL_NUMS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )

    print("* Listening for speech. Press Ctrl+C to stop.")
    
    try:
        while True:
            chunk = stream.read(CHUNK_SIZE)
            yield chunk
    except KeyboardInterrupt:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("* Stopped recording")
        raise StopIteration

async def stream_microphone():
    """Stream microphone data to AWS Transcribe."""
    client = TranscribeStreamingClient(region=REGION)
    
    # Start the transcription stream with Czech language
    stream = await client.start_stream_transcription(
        language_code="cs-CZ",  # Czech language
        media_sample_rate_hz=SAMPLE_RATE,
        media_encoding="pcm",
    )

    async def write_chunks():
        """Send audio chunks from the microphone to AWS."""
        async for chunk in mic_stream():
            await stream.input_stream.send_audio_event(audio_chunk=chunk)
        await stream.input_stream.end_stream()

    # Process transcription events
    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(), handler.handle_events())

if __name__ == "__main__":
    try:
        # Run the async function
        asyncio.run(stream_microphone())
    except Exception as e:
        print(f"Error: {e}")

import os
import django
from django.contrib.auth.hashers import make_password  # Import password hashing
import google.generativeai as genai

# Step 1: Set DJANGO_SETTINGS_MODULE before any Django imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")

# Step 2: Initialize Django settings
django.setup()

from be.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
from api.models import AudioPrompt


def generate_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return str(e)  

if __name__ == "__main__":
    audio_prompt = AudioPrompt.objects.get(id=1)
    print(audio_prompt.transcription)

    #answer = generate_gemini_response("Hello my friend, how are you today?")
    #print(answer)

    

import os
import django
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
    #audio_prompt = AudioPrompt.objects.get(id=1)
    #print(audio_prompt.transcription)

    answer = generate_gemini_response("""You are a highly accurate mathematical answer evaluator. Your task is to determine if a user's plain text answer correctly matches the provided mathematical solution, which will always be in LaTeX format.

**Mathematical Solution (LaTeX format):**
x=1;y=2

**User's Answer (plain text):**
x je 1 a y je 2

**Evaluation Rules:**

1.  The LaTeX mathematical solution is the gold standard.
2.  The user's plain text answer must express the *exact same mathematical meaning* as the LaTeX solution.
3.  The word "je" in the user's answer means "equals" or "is equal to".
4.  The order of variables and values matters. "x je 1" is correct for "x=1", but "1 je x" is correct for "1=x".
5.  Focus solely on the mathematical correctness. Ignore grammatical errors or variations in phrasing, as long as the mathematical meaning is identical.
6. The only output you give is 'true' or 'false'.

**Based on these rules, does the user's answer "x je 1" accurately match the LaTeX solution "x = 1"?**

**Answer with only "true" or "false".**""")
    print(answer.strip())


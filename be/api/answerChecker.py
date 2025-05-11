"""
================================================================================
 Module: answerChecker.py
 Description: 
        Contains logic for validating student answers against correct ones,
        including inline, fraction, variable, and speech-based answers.
 Author: Dominik Horut (xhorut01)
================================================================================
"""

from django.shortcuts import get_object_or_404
from django.db import transaction
import math
import re
from .models import StudentExample, Answer

# Configuration of Gemini API
from be.settings import GEMINI_API_KEY
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

# Exception for handling Gemini API rate limits
class GeminiRateLimitError(Exception):
    pass

# Base class for all answer-checking logic
class AnswerChecker:

    @staticmethod
    def is_valid_answer(answer):
            # Validates if the answer only contains digits, commas, periods, or minus signs
            return bool(re.match(r'^[0-9,.-]+$', answer))

    @staticmethod
    def updateRecord(student_id, example_id, date, duration, correct):
        # Updates the students attempt record for a example and returns if new example can be displayed
        record = get_object_or_404(StudentExample, student_id=student_id, example_id=example_id, date=date)

        try:
            with transaction.atomic():
                record.attempts += 1

            record.duration = duration

            record.solved = correct

            record.save()

            # If the student made 3 attempts or the answer is correct, new example can be displayed
            return record.attempts == 3 or correct

        except Exception as e:
            print({"error": str(e)})

    @staticmethod
    def compareAnswers(student_answer, correct_answer):
        # Compares two answers numerically
        return math.isclose(correct_answer, student_answer, rel_tol=1e-9)
    

    @staticmethod
    def compareAnswersWithGemini(correct_answer, student_answer, prompt):
        # Uses Gemini API to compare students answer transcription with correct answer
        try:
            model = genai.GenerativeModel("gemini-2.0-flash") 
            response = model.generate_content(prompt)

            # Check for API rate limit to use different class for evaluation
            if "quota" in response.text.lower() or "limit" in response.text.lower():
                raise GeminiRateLimitError("API rate limit reached")

            if(response.text.strip().lower() == "true"):
                return True
            else:
                return False 
        
        except Exception as e:
            # Check for API rate limit to use different class for evaluation
            if "429" in str(e) or "quota" in str(e).lower():
                raise GeminiRateLimitError("API rate limit reached")
            else:
                raise 
        
# Checks inline numerical answers
class InlineAnswerChecker(AnswerChecker):
    pass

    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   

        correct_answer = Answer.objects.get(example_id=example_id).answer
        
        # Validate both answers
        if not InlineAnswerChecker.is_valid_answer(correct_answer) or not InlineAnswerChecker.is_valid_answer(student_answer) or not student_answer:
            continue_with_next = AnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next)
        
        # Normalize decimal format
        correct_answer = float(correct_answer.replace(',', '.'))
        student_answer = float(student_answer.replace(',', '.'))
        
        # Compare and update record
        if AnswerChecker.compareAnswers(student_answer, correct_answer):
            # Correct answer
            continue_with_next = AnswerChecker.updateRecord(student_id, example_id, date, duration, True)
            return (True, continue_with_next)
        else:
            # Incorrect answer
            continue_with_next = AnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next)

# Checks fraction-based answers
class FractionAnswerChecker(AnswerChecker):
    pass

    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   

        correct_answer = Answer.objects.get(example_id=example_id).answer

        match = re.match(r"\\frac\{(\d+)\}\{(\d+)\}", correct_answer)

        # Extract numerator and denominator from the correct answers
        if match:
            correct_numerator = float(match.group(1).replace(',', '.'))
            correct_denominator = float(match.group(2).replace(',', '.'))
        else:
            print("Invalid fraction format.")
        
        # Validate students answer and extract numerator and denominator  
        if(FractionAnswerChecker.is_valid_answer(student_answer[0]) and FractionAnswerChecker.is_valid_answer(student_answer[1])):  
            student_numerator = float(student_answer[0].replace(',', '.'))
            student_denominator = float(student_answer[1].replace(',', '.'))
        else:
            continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next)
        
        student_answer = student_numerator / student_denominator
        correct_answer = correct_numerator / correct_denominator

        # Compare and update record
        if AnswerChecker.compareAnswers(correct_answer, student_answer):
            # Correct answer
            continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
            return (True, continue_with_next)
        else:
            # Incorrect answer
            continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next)

# Checks variable-based answers
class VariableAnswerChecker(AnswerChecker):
    pass

    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   

        correct_answer = Answer.objects.get(example_id=example_id).answer

        # Extract variables and their values from the correct answer
        correct_variables = correct_answer.split(';')
        correct_variables = [variable.strip() for variable in correct_variables if variable.strip()]

        correct_values = []
        student_values = []

        # Extract the correct values from the correct answer
        for variable in correct_variables:
            value = variable.split('=')[1].strip()
            correct_values.append(float(value.replace(',', '.'))) 

        # Validate and extract values from the students answer
        for value in student_answer:

            if not value or not VariableAnswerChecker.is_valid_answer(value):
                continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
                return (False, continue_with_next)

            student_values.append(float(value.replace(',', '.')))
        
        # Compare each value
        for i in range(len(correct_values)):

            if not AnswerChecker.compareAnswers(correct_values[i], student_values[i]):
                # One of the values does not match - incorrect answer
                continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
                return (False, continue_with_next)

        # All values match - correct answer
        continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
        return (True, continue_with_next)

# Checks spoken inline numeric answers            
class InlineSpeechAnswerChecker(AnswerChecker):
    pass

    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   
        correct_answer = Answer.objects.get(example_id=example_id).answer

        try:
            correct_answer = float(correct_answer.replace(",", "."))
        except ValueError:
            return (False, False)

        student_answer = student_answer.replace(",", ".")

        # Extract all numbers from the spoken answer
        numbers_in_answer = re.findall(r'\d+\.\d+|\d+', student_answer)
        extracted_numbers = [float(num) for num in numbers_in_answer]

        correct_number = None
        is_correct = False

        # Check if any of the extracted numbers match the correct answer
        for num in extracted_numbers:
            if AnswerChecker.compareAnswers(num, correct_answer):
                is_correct = True
                correct_number = num
                break  # stop at the first correct number

        # If no correct number was found, use the last extracted number to be displayed to user
        if not is_correct and extracted_numbers:
            correct_number = extracted_numbers[-1] 

        continue_with_next = InlineSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, is_correct)

        return (is_correct, continue_with_next, correct_number)

# Checks spoken fraction-based answers
class FractionSpeechAnswerChecker(AnswerChecker):
    
    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   
        correct_answer = Answer.objects.get(example_id=example_id).answer
        print(student_answer)
        match = re.match(r"\\frac\{(\d+)\}\{(\d+)\}", correct_answer)
        
        # Extract numerator and denominator from the correct answers
        if match:
            correct_numerator = float(match.group(1).replace(',', '.'))
            correct_denominator = float(match.group(2).replace(',', '.'))
        else:
            return (False, False) 

        # Extract all numbers from the spoken answer
        numbers_in_answer = re.findall(r'\d+\.\d+|\d+', student_answer)

        if not numbers_in_answer:
            return (False, False) 

        student_fractions = []
        i = 0
        # Create fractions from extracted numbers in pairs (numerator, denominator)
        while i < len(numbers_in_answer) - 1:
            numerator = float(numbers_in_answer[i].replace(',', '.'))
            denominator = float(numbers_in_answer[i+1].replace(',', '.'))
            student_fractions.append((numerator, denominator))
            i += 2 

        # Compare each fraction with the correct answer
        for student_numerator, student_denominator in student_fractions:
            if (AnswerChecker.compareAnswers(correct_numerator, student_numerator) and 
                AnswerChecker.compareAnswers(correct_denominator, student_denominator)):
                # Correct answer
                continue_with_next = FractionSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
                return (True, continue_with_next, {"numerator": student_numerator, "denominator": student_denominator})
        # Incorrect answer
        continue_with_next = FractionSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
        return (False, continue_with_next, {"numerator": student_fractions[-1][0], "denominator": student_fractions[-1][1]})

# Checks spoken variable-based answers
class VariableSpeechAnswerChecker(AnswerChecker):
    
    @staticmethod   
    def verifyAnswer(student_id, example_id, date, duration, student_answer):

        correct_answer = Answer.objects.get(example_id=example_id).answer
        correct_variables = correct_answer.split(';')
        correct_variables = [variable.strip() for variable in correct_variables if variable.strip()]

        correct_values = []
        student_values = []
        
        # Extract the values from the correct answer
        for variable in correct_variables:
            value = variable.split('=')[1].strip()  # Extract value after '='
            correct_values.append(float(value.replace(',', '.')))  # Store as float

        # Extract values from the spoken answer
        student_matches = re.findall(r"([a-zA-Z]+)\s*(rovná se|je)\s*([\d,]+)", student_answer, re.IGNORECASE)
        
        for match in student_matches:
            student_value_str = match[2].replace(',', '.')  
            try:
                student_value = float(student_value_str) 
            except ValueError:
                student_value = 0.0
            student_values.append(student_value)

        # Compare sorted lists of values
        if sorted(correct_values) == sorted(student_values): 
            # All values match - correct answer
            continue_with_next = VariableSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
            return (True, continue_with_next, student_values)
        else:
            # One of the values does not match - incorrect answer
            continue_with_next = VariableSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next, student_values)

# Checks spoken answer using LLM (Gemini)
class LLMAnswerChecker(AnswerChecker):
    
    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer, input_type):
        correct_answer = Answer.objects.get(example_id=example_id).answer

        # Choose prompt based on the input type
        if input_type == "fraction":
            prompt = f"""There is a math example with answer written in Latex: {correct_answer}, the user told the answer by voice in czech language: {student_answer}. 
                         Is the users answer correct? Answer just true or false."""
        elif input_type == "variable":
            prompt = f"""Evaluate LaTeX math answer. 
                        Correct answer in LaTeX: {correct_answer}
                        User's Czech voice answer: {student_answer}

                        Rules:
                        - Match each variable name exactly
                        - Compare all variable values
                        - Case-sensitive comparison

                        Respond only "true" or "false"."""

        is_correct = LLMAnswerChecker.compareAnswersWithGemini(correct_answer, student_answer, prompt)
            
        if(is_correct):
            # Correct answer
            continue_with_next = LLMAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
            return (True, continue_with_next, "")
        else:
            # Incorrect answer
            continue_with_next = LLMAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next, "")
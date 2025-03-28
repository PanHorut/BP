from django.shortcuts import get_object_or_404
from django.db import transaction
import math
import re

from .models import StudentExample, Example, Answer



from be.settings import GEMINI_API_KEY
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

class GeminiRateLimitError(Exception):
    pass

class AnswerChecker:

    @staticmethod
    def updateRecord(student_id, example_id, date, duration, correct):
        record = get_object_or_404(StudentExample, student_id=student_id, example_id=example_id, date=date)

        try:
            with transaction.atomic():
                record.attempts += 1

            record.duration = duration

            record.solved = correct

            record.save()

            # student ma 3 pokusy na vyreseni prikladu, pokud true, signalizuje se pokracovani na dalsi priklad
            return record.attempts == 3 or correct

        except Exception as e:
            print({"error": str(e)})

    @staticmethod
    def compareAnswers(student_answer, correct_answer):
        return math.isclose(correct_answer, student_answer, rel_tol=1e-9)
    


    def compareAnswersWithGemini(correct_answer, student_answer, prompt):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash") # nebo asi vic accurate gemini-2.0-flash a gemini-1.5-flash se da fine-tunovat
            response = model.generate_content(prompt)

            if "quota" in response.text.lower() or "limit" in response.text.lower():
                raise GeminiRateLimitError("API rate limit reached")

            if(response.text.strip().lower() == "true"):
                return True
            else:
                return False 
        
        except Exception as e:
            # Detect rate limit specific exceptions
            if "429" in str(e) or "quota" in str(e).lower():
                raise GeminiRateLimitError("API rate limit reached")
            else:
                # For non-rate limit errors, re-raise the exception
                raise 
        

class InlineAnswerChecker(AnswerChecker):
    pass

    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   

        def is_valid_answer(answer):
            return bool(re.match(r'^[0-9,.-]+$', answer))

        correct_answer = Answer.objects.get(example_id=example_id).answer

        if not is_valid_answer(correct_answer) or not is_valid_answer(student_answer) or not student_answer:
            continue_with_next = AnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next)

        correct_answer = float(correct_answer.replace(',', '.'))
        student_answer = float(student_answer.replace(',', '.'))
        

        if AnswerChecker.compareAnswers(student_answer, correct_answer):
            continue_with_next = AnswerChecker.updateRecord(student_id, example_id, date, duration, True)
            return (True, continue_with_next)
        else:
            continue_with_next = AnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next)

class FractionAnswerChecker(AnswerChecker):
    pass

    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   

        correct_answer = Answer.objects.get(example_id=example_id).answer

        match = re.match(r"\\frac\{(\d+)\}\{(\d+)\}", correct_answer)
        if match:
            correct_numerator = float(match.group(1).replace(',', '.'))
            correct_denominator = float(match.group(2).replace(',', '.'))
        else:
            print("Invalid fraction format.")
        
        student_numerator = float(student_answer[0].replace(',', '.'))
        student_denominator = float(student_answer[1].replace(',', '.'))

        if AnswerChecker.compareAnswers(correct_numerator, student_numerator) and AnswerChecker.compareAnswers(correct_denominator, student_denominator):
            continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
            return (True, continue_with_next)
        else:
            continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next)

class VariableAnswerChecker(AnswerChecker):
    pass

    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   

        correct_answer = Answer.objects.get(example_id=example_id).answer

        correct_variables = correct_answer.split(';')
        correct_variables = [variable.strip() for variable in correct_variables if variable.strip()]

        correct_values = []
        student_values = []

       

        for variable in correct_variables:
            value = variable.split('=')[1].strip()
            correct_values.append(float(value.replace(',', '.'))) 

        for value in student_answer:

            # nevyplnena hodnota -> spatne
            if not value:
                continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
                return (False, continue_with_next)

            student_values.append(float(value.replace(',', '.')))

        for i in range(len(correct_values)):

            if not AnswerChecker.compareAnswers(correct_values[i], student_values[i]):
                continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
                return (False, continue_with_next)

        continue_with_next = FractionAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
        return (True, continue_with_next)
            
class InlineSpeechAnswerChecker(AnswerChecker):
    pass

    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   
        correct_answer = Answer.objects.get(example_id=example_id).answer

        try:
            correct_answer = float(correct_answer.replace(",", "."))
        except ValueError:
            print("Invalid correct answer format.")
            return (False, False)

        student_answer = student_answer.replace(",", ".")

        numbers_in_answer = re.findall(r'\d+\.\d+|\d+', student_answer)
        
        extracted_numbers = [float(num) for num in numbers_in_answer]

        print(f"Extracted Numbers: {extracted_numbers}, Correct Answer: {correct_answer}")

        correct_number = None
        is_correct = False

        for num in extracted_numbers:
            if AnswerChecker.compareAnswers(num, correct_answer):
                is_correct = True
                correct_number = num
                break  # Stop at the first correct number

        if not is_correct and extracted_numbers:
            correct_number = extracted_numbers[-1] 

        continue_with_next = InlineSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, is_correct)

        return (is_correct, continue_with_next, correct_number)

class FractionSpeechAnswerChecker(AnswerChecker):
    
    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer):   
        correct_answer = Answer.objects.get(example_id=example_id).answer
        print(student_answer)
        match = re.match(r"\\frac\{(\d+)\}\{(\d+)\}", correct_answer)
        
        if match:
            correct_numerator = float(match.group(1).replace(',', '.'))
            correct_denominator = float(match.group(2).replace(',', '.'))
        else:
            print("Invalid fraction format.")
            return (False, False) 

        numbers_in_answer = re.findall(r'\d+\.\d+|\d+', student_answer)

        if not numbers_in_answer:
            print("Invalid student fraction format.")
            return (False, False) 

        student_fractions = []
        i = 0
        while i < len(numbers_in_answer) - 1:
            numerator = float(numbers_in_answer[i].replace(',', '.'))
            denominator = float(numbers_in_answer[i+1].replace(',', '.'))
            student_fractions.append((numerator, denominator))
            i += 2  # dalsi par citatel a jmenovatel = +2

        for student_numerator, student_denominator in student_fractions:
            if (AnswerChecker.compareAnswers(correct_numerator, student_numerator) and 
                AnswerChecker.compareAnswers(correct_denominator, student_denominator)):
                
                continue_with_next = FractionSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
                return (True, continue_with_next, {"numerator": student_numerator, "denominator": student_denominator})

        continue_with_next = FractionSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
        return (False, continue_with_next, {"numerator": student_fractions[-1][0], "denominator": student_fractions[-1][1]})

class VariableSpeechAnswerChecker(AnswerChecker):
    
    @staticmethod   
    def verifyAnswer(student_id, example_id, date, duration, student_answer):

        correct_answer = Answer.objects.get(example_id=example_id).answer
        
        # Split the correct answer based on semicolons (e.g., "x=8; y=4")
        correct_variables = correct_answer.split(';')
        correct_variables = [variable.strip() for variable in correct_variables if variable.strip()]


        # Initialize lists to store the correct values and student values
        correct_values = []
        student_values = []
        
        # Extract the correct values from the correct answer
        for variable in correct_variables:
            value = variable.split('=')[1].strip()  # Extract value after '='
            correct_values.append(float(value.replace(',', '.')))  # Store as float

        # Now extract all variables and their values from the student's answer
        student_matches = re.findall(r"([a-zA-Z]+)\s*(rovná se|je)\s*([\d,]+)", student_answer, re.IGNORECASE)
        
        # Store the student's extracted values
        for match in student_matches:
            student_value_str = match[2].replace(',', '.')  # Ensure decimal uses dot
            try:
                student_value = float(student_value_str)  # Convert to float
            except ValueError:
                student_value = 0.0  # In case of any issue with conversion, default to 0.0
            student_values.append(student_value)

        print(f"Correct values: {correct_values}, Student values: {student_values}")
        if sorted(correct_values) == sorted(student_values): 
            continue_with_next = VariableSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
            return (True, continue_with_next, student_values)
        else:
            continue_with_next = VariableSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next, student_values)

class LLMAnswerChecker(AnswerChecker):
    
    @staticmethod
    def verifyAnswer(student_id, example_id, date, duration, student_answer, input_type):
        correct_answer = Answer.objects.get(example_id=example_id).answer
        print(correct_answer)
        
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
            continue_with_next = LLMAnswerChecker.updateRecord(student_id, example_id, date, duration, True)
            return (True, continue_with_next, "")
        else:
            continue_with_next = LLMAnswerChecker.updateRecord(student_id, example_id, date, duration, False)
            return (False, continue_with_next, "")

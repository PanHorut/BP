from django.shortcuts import get_object_or_404
from django.db import transaction
import math
import re
from .models import StudentExample, Example, Answer

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

        # Convert correct answer to float
        try:
            correct_answer = float(correct_answer.replace(",", "."))
        except ValueError:
            print("Invalid correct answer format.")
            return (False, False)

        # Normalize student's answer (replace ',' with '.' for decimal numbers)
        student_answer = student_answer.replace(",", ".")

        # Extract all numbers (integers and decimals) from student's answer
        numbers_in_answer = re.findall(r'\d+\.\d+|\d+', student_answer)
        
        # Convert extracted numbers to floats
        extracted_numbers = [float(num) for num in numbers_in_answer]

        print(f"Extracted Numbers: {extracted_numbers}, Correct Answer: {correct_answer}")

        # Check if any extracted number matches the correct answer
        is_correct = any(AnswerChecker.compareAnswers(num, correct_answer) for num in extracted_numbers)

        # Update the record based on whether the answer is correct
        continue_with_next = InlineSpeechAnswerChecker.updateRecord(student_id, example_id, date, duration, is_correct)

        return (is_correct, continue_with_next)
    
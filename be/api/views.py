from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Task, Example, Answer, Student, Skill, ExampleSkill, StudentExample
from .serializers import ExampleSerializer, ExampleSkillSerializer, SkillSerializer, TaskSerializer, RecordInitSerializer
from django.http import JsonResponse
from django.db.models import Prefetch
import json
import random





class ExampleList(generics.ListCreateAPIView):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer

class SkillList(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ExampleSkillList(generics.ListCreateAPIView):
    queryset = ExampleSkill.objects.all()
    serializer_class = ExampleSkillSerializer



@api_view(['POST'])
def addExample(request):
    # Extract skill IDs, task name, example details, and answer from the request data
    skill_ids = request.data.get('skill_ids', [])
    task_name = request.data.get('task_name')
    example_text = request.data.get('example')  # The example content
    input_type = request.data.get('input_type')  # The input type for the example
    answer_text = request.data.get('answer')  # The answer text

    # Ensure the task name and example are provided
    if not task_name:
        return Response({"error": "Task name is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not example_text or not input_type:
        return Response({"error": "Example text and input type are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create or retrieve the Task instance
    task_instance, created = Task.objects.get_or_create(name=task_name)

    # Create the Example instance
    example_data = {
        'example': example_text,
        'input_type': input_type,
        'task': task_instance.id  # Link to the task instance
    }
    example_serializer = ExampleSerializer(data=example_data)
    if example_serializer.is_valid():
        example_instance = example_serializer.save()

        # If an answer is provided, create the Answer instance
        if answer_text:
            Answer.objects.create(example=example_instance, answer=answer_text)

        # Create ExampleSkill instances for each skill ID provided
        for skill_id in skill_ids:
            ExampleSkill.objects.create(example=example_instance, skill_id=skill_id)

        return Response(example_serializer.data, status=status.HTTP_201_CREATED)

    return Response(example_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_all_skills(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_parent_skills(request):

    parent_skills = Skill.objects.filter(parent_skill__isnull=True)
    serializer = SkillSerializer(parent_skills, many=True)
    
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_leaf_skills(request):
    leaf_skills = Skill.objects.filter(dependent_skills__isnull=True)
    
    serializer = SkillSerializer(leaf_skills, many=True)
    
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_skill(request, skill_id):
    try:
    
        parent_skill = Skill.objects.get(id=skill_id)

        child_skills = Skill.objects.filter(parent_skill=parent_skill)
 
        parent_skill_data = SkillSerializer(parent_skill).data
        child_skills_data = SkillSerializer(child_skills, many=True).data
        
        response_data = {
            'skill': parent_skill_data,
            'child_skills': child_skills_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    except Skill.DoesNotExist:
        return Response({"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_examples(request):
    topics = request.query_params.get('topics')

    if not topics:
        return Response({"error": "No topics provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        topics_data = json.loads(topics)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format for topics"}, status=status.HTTP_400_BAD_REQUEST)

    example_data = []

    for topic in topics_data:
        skill_id = topic.get('id')
        count = topic.get('count')

        if not skill_id or not count:
            return Response({"error": "Skill ID or count missing in topics"}, status=status.HTTP_400_BAD_REQUEST)

        count = int(count)  # Convert count to integer
        examples = Example.objects.filter(exampleskill__skill__id=skill_id).order_by('?').distinct()[:count]
        for example in examples:
            example_data.append({
                "id": example.id,
                "example": example.example,
                "input_type": example.input_type,
                "answers": [
                    {
                        "id": answer.id,
                        "answer": answer.answer
                    }
                    for answer in example.answers.all()
                ]
            })

    # Shuffle the final list of examples to ensure they are mixed
    random.shuffle(example_data)

    return Response(example_data, status=status.HTTP_200_OK)


# vytvori zaznam, ze zak dany priklad pocital, datum se nastavi automaticky
@api_view(['POST'])
def create_example_record(request):
    student = request.data.get('student_id')
    example = request.data.get('example_id')
    
    if not student:
        return Response({"error": "Student ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not example:
        return Response({"error": "Example ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    init_data = {
        'student': student,
        'example': example
    }

    record_init_serializer = RecordInitSerializer(data=init_data)

    if record_init_serializer.is_valid():
        record = record_init_serializer.save()

        response_data = record_init_serializer.data
        response_data['date'] = record.date  # Include the 'date' from the saved record

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(record_init_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# pokud dite u prikladu odpovi, na zaklade spravnosti se urci co dal (dalsi pokus x spravna odpoved x dalsi priklad)
@api_view(['POST'])
def update_example_record(request):

    is_correct = request.data.get('isCorrect')
    student = request.data.get('student_id')
    example = request.data.get('example_id')
    date = request.data.get('date')
    duration = request.data.get('time')
  

    if not student or not example or not duration:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    student_example = get_object_or_404(StudentExample, student_id=student, example_id=example, date=date)
    
    try:
        with transaction.atomic():
            student_example.attempts += 1

            student_example.duration = duration

            next_example = student_example.attempts == 3
            
                                    
            student_example.save()
        
        return Response({"message": "Record updated successfully", "next_example": next_example}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def delete_example_record(request):
    student = request.data.get('student_id')
    example = request.data.get('example_id')
    date = request.data.get('date')

    if not student or not example or not date:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    student_example = get_object_or_404(StudentExample, student_id=student, example_id=example, date=date)

    try:
        with transaction.atomic():
            student_example.delete()

        return Response({"message": "Record successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

    except StudentExample.DoesNotExist:
        return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def skip_example(request):
    student = request.data.get('student_id')
    example = request.data.get('example_id')
    date = request.data.get('date')

    if not student or not example or not date:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    student_example = get_object_or_404(StudentExample, student_id=student, example_id=example, date=date)

    try:
        with transaction.atomic():
            student_example.skipped = True
            student_example.attempts = 0
            student_example.duration = 0
                        
            student_example.save()
        
        return Response({"message": "Example skipped"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_tasks(request):
    # Prefetch the related data: examples, answers, and example skills
    example_skills = Prefetch('exampleskill_set', queryset=ExampleSkill.objects.select_related('skill'))
    tasks = Task.objects.prefetch_related(
        'example_set__answers',        # Fetch related answers
        'example_set__exampleskill_set'  # Prefetch related ExampleSkills
    )

    # Prepare the response data
    data = [
        {
            "task_id": task.id,
            "task_name": task.name,
            "examples": [
                {
                    "example_id": example.id,
                    "example_text": example.example,
                    "input_type": example.input_type,
                    "answers": [
                        {
                            "answer_id": answer.id,
                            "answer_text": answer.answer
                        }
                        for answer in example.answers.all()
                    ],
                    "skills": [
                        {
                            "skill_id": example_skill.skill.id,
                            "skill_name": example_skill.skill.name
                        }
                        for example_skill in example.exampleskill_set.all()
                    ]
                }
                for example in task.example_set.all()
            ]
        }
        for task in tasks
    ]

    # Return the data as JSON
    return JsonResponse(data, safe=False)

@api_view(['DELETE'])
def delete_example(request, example_id):
    # Get the example object, or return 404 if not found
    example = get_object_or_404(Example, id=example_id)
    
    try:
        # Start a database transaction to ensure consistency
        with transaction.atomic():
            # Delete the example
            example.delete()
        
        # Return a successful response with no content
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        # In case of an error, return an internal server error response
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_task(request, task_id):

    try:
        # Start a transaction to ensure consistency
        with transaction.atomic():
            # Fetch the task by ID
            task = get_object_or_404(Task, id=task_id)

            # Delete the task and all related objects (Examples, Answers, etc.)
            task.delete()

        # If successful, return a 204 No Content response
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        # Handle any potential errors (e.g., foreign key constraint issues, etc.)
        return Response(
            {"error": f"Error deleting task: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def create_skill(request):
    try:
        # Extract data from the request
        name = request.data.get('name')
        parent_skill_id = request.data.get('parent_skill')  # Optional

        if not name:
            return Response({"error": "Skill name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and fetch the parent skill if provided
        parent_skill = None
        if parent_skill_id:
            parent_skill = get_object_or_404(Skill, id=parent_skill_id)

        # Create the new skill
        with transaction.atomic():  # Ensure transactional consistency
            skill = Skill.objects.create(name=name, parent_skill=parent_skill)

        # Serialize and return the created skill data
        return JsonResponse({
            "id": skill.id,
            "name": skill.name,
            "parent_skill": skill.parent_skill.id if skill.parent_skill else None,
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Handle any unexpected errors
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

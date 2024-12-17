from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Task, Example, Answer, Student, Skill, ExampleSkill, StudentExample
from .serializers import ExampleSerializer, ExampleSkillSerializer, SkillSerializer, TaskSerializer, RecordInitSerializer



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
    skill_ids = request.query_params.getlist('skill_ids')

    if not skill_ids:
        return Response({"error": "No skill IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Get all examples that have the given skill IDs
    examples = Example.objects.filter(exampleskill__skill__id__in=skill_ids).distinct()

    # Serialize the examples along with their answers
    example_data = [
        {
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
        }
        for example in examples
    ]

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
        

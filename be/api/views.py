from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Example
from .models import Skill
from .models import ExampleSkill
from .models import Task
from .serializers import ExampleSerializer
from .serializers import SkillSerializer
from .serializers import ExampleSkillSerializer
from .serializers import TaskSerializer


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
    # Extract skill IDs and task name from the request data
    skill_ids = request.data.get('skill_ids', [])
    task_name = request.data.get('task_name')  # Get the task name from the request data

    # Create the Task instance
    if task_name:
        task_instance, created = Task.objects.get_or_create(name=task_name)  # Avoid duplicates based on name
    else:
        return Response({"error": "Task name is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Prepare the example data with the task ID
    example_data = request.data.copy()
    example_data['task'] = task_instance.id  # Assign task ID to the example

    # Create the Example instance
    serializer = ExampleSerializer(data=example_data)
    if serializer.is_valid():
        example_instance = serializer.save()  # Save the example with the associated task

        # Create ExampleSkill instances for each skill
        for skill_id in skill_ids:
            ExampleSkill.objects.create(example=example_instance, skill_id=skill_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    # Serialize the examples (you can adjust the serialization according to your needs)
    example_data = [
        {
            "id": example.id,
            "example": example.example,
            "answer": example.answer,
            "input_type": example.input_type
        }
        for example in examples
    ]

    return Response(example_data, status=status.HTTP_200_OK)

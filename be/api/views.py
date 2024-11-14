from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Example
from .models import Skill
from .models import ExampleSkill
from .models import Task
from .models import Answer
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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Example, Answer, Skill, ExampleSkill
from .serializers import ExampleSerializer, AnswerSerializer

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

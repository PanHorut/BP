from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Task, Example, Answer, Student, Skill, ExampleSkill, StudentExample, Admin, Step
from .serializers import ExampleSerializer, ExampleSkillSerializer, SkillSerializer, TaskSerializer, RecordInitSerializer
from django.http import JsonResponse
from django.db.models import Prefetch
from .utils import get_height, build_skill_tree, get_skill_paths
from django.contrib.auth.hashers import make_password, check_password
from .answerChecker import InlineAnswerChecker, FractionAnswerChecker, VariableAnswerChecker

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

def create_skill_relations(skill_ids):

    skills = Skill.objects.filter(id__in=skill_ids)

    for skill in skills:
        # Get skills that are NOT the same and have a DIFFERENT skill_type
        related_skills = [s for s in skills if s != skill and s.skill_type != skill.skill_type]
        skill.related_skills.add(*related_skills)  

@api_view(['POST'])
def create_task(request):
    task_name = request.data.get('task_name')
    skill_ids = request.data.get('skill_ids', [])
    examples_data = request.data.get('examples', [])  # Array of examples

    # Ensure the task name is provided
    if not task_name:
        return Response({"error": "Nebyl zadán název sady"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch skills
    skills = Skill.objects.filter(id__in=skill_ids)

    if not skills.exists():
        return Response({"error": "At least one valid skill ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Create or retrieve the Task instance
    task_instance, created = Task.objects.get_or_create(name=task_name)

    # Assign skills to the task
    task_instance.skills.add(*skills)

    # List to store created examples data
    created_examples = []

    # Loop through each example in the request data
    for example_data in examples_data:
        example_text = example_data.get('example')
        input_type = example_data.get('input_type')
        answer_text = example_data.get('answer')
        steps = example_data.get('steps', [])

        # Validate required fields
        if not example_text or not input_type:
            continue  # Skip this example if required fields are missing

        # Prepare example data for serializer
        example_payload = {
            'example': example_text,
            'input_type': input_type,
            'task': task_instance.id  # Link to the task instance
        }
        example_serializer = ExampleSerializer(data=example_payload)
        
        if example_serializer.is_valid():
            with transaction.atomic():  # Ensures atomic database operations
                example_instance = example_serializer.save()

                # If an answer is provided, create the Answer instance
                if answer_text:
                    Answer.objects.create(example=example_instance, answer=answer_text)

                # Create ExampleSkill instances for each skill ID provided
                for skill in skills:
                    ExampleSkill.objects.create(example=example_instance, skill=skill)
                
                create_skill_relations(skill_ids)

                # Create Step instances
                for index, step_text in enumerate(steps, start=1):
                    if step_text:  # Check if step is not an empty string
                        Step.objects.create(
                            example=example_instance,
                            text=step_text,
                            order=index  
                        )

                # Add the created example data to the list
                created_examples.append(example_serializer.data)
    
    # Return all created examples
    return Response({"created_examples": created_examples}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def edit_task(request):
    task_id = request.data.get('task_id')
    task_name = request.data.get('task_name')
    skill_ids = request.data.get('skill_ids', [])
    examples_data = request.data.get('examples', [])  # Array of examples

    # Ensure the task ID is provided
    if not task_id:
        return Response({"error": "Nebyl zadán ID sady"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the existing task by ID
    try:
        task_instance = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    # Update task name if provided
    if task_name:
        task_instance.name = task_name
        task_instance.save()

    # Fetch skills
    skills = Skill.objects.filter(id__in=skill_ids)
    if not skills.exists():
        return Response({"error": "At least one valid skill ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Update task's skills
    task_instance.skills.set(skills)  # Replace old skills with new ones

    # List to store updated examples data
    updated_examples = []

    # Loop through each example in the request data
    for example_data in examples_data:
        example_id = example_data.get('example_id')
        example_text = example_data.get('example')
        input_type = example_data.get('input_type')
        answer_text = example_data.get('answer')
        steps = example_data.get('steps', [])

        # Validate required fields
        if not example_text or not input_type:
            continue  # Skip this example if required fields are missing
        
        # If example_id is provided, try to update the existing example
        if example_id:
            try:
                example_instance = Example.objects.get(id=example_id, task=task_instance)
                example_instance.example = example_text
                example_instance.input_type = input_type
                example_instance.save()
            except Example.DoesNotExist:
                return Response({"error": f"Example with ID {example_id} not found."},
                                status=status.HTTP_404_NOT_FOUND)
        
        # If no example_id is provided, check by example text or create a new one
        else:
            example_instance, created = Example.objects.update_or_create(
                example=example_text,
                task=task_instance,
                defaults={'input_type': input_type}
            )

        # Update or create answer
        if answer_text:
            answer_instance, _ = Answer.objects.update_or_create(
                example=example_instance,
                defaults={'answer': answer_text}
            )

        # Update or create ExampleSkill instances
        for skill in skills:
            ExampleSkill.objects.update_or_create(example=example_instance, skill=skill)
        
        # Create or update skill relations
        create_skill_relations(skill_ids)

        # Update or create Step instances
        Step.objects.filter(example=example_instance).delete()  # Clear old steps first
        for index, step_text in enumerate(steps, start=1):
            if step_text:  # Only create steps that are not empty
                Step.objects.create(
                    example=example_instance,
                    order=index,
                    text=step_text
                )

        # Add the updated example data to the list
        example_serializer = ExampleSerializer(example_instance)
        updated_examples.append(example_serializer.data)

    # Return all updated examples
    return Response({"updated_examples": updated_examples}, status=status.HTTP_200_OK)


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
    leaf_skills = Skill.objects.filter(subskills__isnull=True)
    
    serializer = SkillSerializer(leaf_skills, many=True)
    
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_skill(request, skill_id):
    try:
    
        skill = Skill.objects.get(id=skill_id)
        skill_data = SkillSerializer(skill).data
    
        
        return Response(skill_data, status=status.HTTP_200_OK)
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

    # Assuming get_skill_paths returns an array like [[65, 69, 70], [66, 69, 70]]
    skill_paths = get_skill_paths(topics_data)
    print(skill_paths)
    example_data = []

    # For each skill path (e.g., [65, 69, 70]), filter the examples
    for path in skill_paths:
        # First, find all examples that have *at least* one skill in the path
        examples = Example.objects.filter(
            exampleskill__skill__id__in=path
        ).distinct()

        for example in examples:
            # Get all skill IDs associated with this example through ExampleSkill
            example_skill_ids = set(example.exampleskill_set.values_list('skill__id', flat=True))

            # Check if the example skill IDs contain all the skills in the current path (no missing skills)
            if example_skill_ids.issuperset(set(path)):
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
                    ],
                    "steps": [
                        {
                            "id": step.id,
                            "order": step.order,
                            "text": step.text
                        }
                        for step in example.steps.all().order_by('order')
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
    # Prefetch related data for optimization
    example_skills = Prefetch('exampleskill_set', queryset=ExampleSkill.objects.select_related('skill'))
    example_steps = Prefetch('steps', queryset=Step.objects.order_by('order'))  # Order by 'order' field

    tasks = Task.objects.prefetch_related(
        'example_set__answers',          # Fetch related answers
        'example_set__exampleskill_set', # Prefetch related ExampleSkills
        'example_set__steps'          # Prefetch related Steps
    )

    # Prepare the response data
    data = [
        {
            "task_id": task.id,
            "task_name": task.name,
            "examples": [
                {
                    "example_id": example.id,
                    "example": example.example,
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
                            "id": example_skill.skill.id,
                            "name": example_skill.skill.name,
                            "height": example_skill.skill.height,
                            "skill_type": example_skill.skill.skill_type,
                            "parent_skill": example_skill.skill.parent_skill.id if example_skill.skill.parent_skill else None,
                            "related_skills": list(example_skill.skill.related_skills.values_list('id', flat=True))
                        }
                        for example_skill in example.exampleskill_set.all()
                    ],
                    "steps": [
                        {
                            "step_id": step.id,
                            "step_text": step.text,
                            "order": step.order
                        }
                        for step in example.steps.all()
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
        with transaction.atomic():
            # Fetch the task by ID
            task = get_object_or_404(Task, id=task_id)
            
            # Get all skills related to this task before deleting it
            related_skills = list(task.skills.all())  

            # Remove connections from the skill-task relationship table
            task.skills.clear()

            # Delete the task (this will also delete related Examples and Answers)
            task.delete()

            # Check skill relationships and remove them if no other task uses them
            for skill in related_skills:
                for related_skill in skill.related_skills.all():
                    # Get all tasks where both skills are used together
                    shared_tasks = Task.objects.filter(skills=skill).filter(skills=related_skill)
                    
                    # If this was the last task using this relationship, remove the relation
                    if not shared_tasks.exists():
                        skill.related_skills.remove(related_skill)
                        related_skill.related_skills.remove(skill)  # Ensure bidirectional removal

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response(
            {"error": f"Error deleting task: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def create_skill(request):
    try:
        # Extract data from the request
        name = request.data.get('name')
        parent_skill_id = request.data.get('parent_skill') 
        

        if not name:
            return Response({"error": "Skill name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and fetch the parent skill if provided
        parent_skill = None
        skill_type = None  # Default is None (NULL)

        if parent_skill_id:
            parent_skill = get_object_or_404(Skill, id=parent_skill_id)
            skill_type = parent_skill.skill_type  
            height = get_height(parent_skill_id) + 1
        
        # Create the new skill
        with transaction.atomic():  # Ensure transactional consistency
            
            skill = Skill.objects.create(name=name, parent_skill=parent_skill, skill_type=skill_type, height=height)
            
        # Serialize and return the created skill data
        return JsonResponse({
            "id": skill.id,
            "name": skill.name,
            "parent_skill": skill.parent_skill.id if skill.parent_skill else None,
            "skill_type": skill.skill_type,  # Include skill_type in response
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Handle any unexpected errors
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_skill_tree(request):
    skills = Skill.objects.all()
    skill_list = SkillSerializer(skills, many=True).data

    # Convert the flat list into a hierarchical structure
    skill_dict = {skill["id"]: {**skill, "children": []} for skill in skill_list}

    root_skills = []
    for skill in skill_dict.values():
        if skill["parent_skill"] is None:
            root_skills.append(skill)
        else:
            parent = skill_dict.get(skill["parent_skill"])
            if parent:
                parent["children"].append(skill)

    return Response(root_skills)

@api_view(['GET'])
def search_skills(request):
    query = request.GET.get('q', '')

    if not query:
        return Response([])

    # Filter skills by name (case insensitive)
    skills = Skill.objects.filter(name__icontains=query)
    
    # Serialize the skills
    skill_list = SkillSerializer(skills, many=True).data

    return Response(skill_list)

@api_view(['GET'])
def get_landing_page_skills(request):
    skills = Skill.objects.filter(height=3) 
    serializer = SkillSerializer(skills, many=True)  
    return Response(serializer.data) 

@api_view(['GET'])
def get_related_skills_tree(request, skill_id):
    try:
        main_skill = Skill.objects.get(id=skill_id)  # Get the selected skill
        visited = set()  # Track visited nodes to avoid infinite recursion
        tree = []

        # Get all directly related skills
        related_skills = main_skill.related_skills.all()

        # Build tree structure by ensuring parent-child hierarchy
        for skill in related_skills:
            skill_ids = [main_skill.id, skill.id]  # Include main_skill and related skill IDs
            if skill.id not in visited:
                subtree = build_skill_tree(skill, visited, skill_ids, related_skills, None)
                if subtree:
                    tree.append(subtree)

        return Response(tree)  # Return JSON tree response
    except Skill.DoesNotExist:
        return Response({"error": "Skill not found"}, status=404)
    
@api_view(['GET'])
def get_children_skills_tree(request, skill_id):
    withCounts = request.GET.get('with_counts', 'false') == 'true'
    print(withCounts)

    try:
        main_skill = Skill.objects.get(id=skill_id)  # Get the selected skill
        visited = set()  # Track visited nodes to avoid infinite recursion
        tree = []

        # Get all directly related child skills (children of the skill_id)
        children = Skill.objects.filter(parent_skill=main_skill)

        # Build tree structure for the given skill and its children
        for skill in children:
            if skill.id not in visited:
                subtree = build_skill_tree(skill, visited, None, None, withCounts)  # Use your existing tree-building logic
                if subtree:
                    tree.append(subtree)

        return Response(tree)  # Return JSON tree response
    except Skill.DoesNotExist:
        return Response({"error": "Skill not found"}, status=404)

@api_view(['GET'])
def get_operation_skills(request, skill_id):
    try:
        main_skill = get_object_or_404(Skill, id=skill_id)

        # Get children of the main skill
        children_skills = main_skill.subskills.all()

        # Get related operation skills of the main skill
        related_operation_skills = main_skill.related_skills.filter(skill_type='OPERATION')

        # Prepare response data
        skills_data = []

        for operation_skill in related_operation_skills:
            child_data = []

            for child_skill in children_skills:
                # Count examples that have BOTH operation_skill and child_skill
                examples_count = ExampleSkill.objects.filter(
                    skill=operation_skill
                ).filter(
                    example__in=ExampleSkill.objects.filter(skill=child_skill).values('example')
                ).count()

                child_data.append({
                    "related_id": child_skill.id,
                    "related_name": child_skill.name,
                    "examples": examples_count
                })

            skills_data.append({
                "id": operation_skill.id,
                "name": operation_skill.name,
                "related_skills": child_data  # List of children with their common examples count
            })

        return Response(skills_data)
    
    except Skill.DoesNotExist:
        return Response({"error": "Skill not found"}, status=404)

@api_view(['POST'])
def register_student(request):
    username = request.data.get('username')
    passphrase = request.data.get('passphrase')

    if not username or not passphrase:
        return Response({'error': 'Username and passphrase are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Student.objects.filter(username=username).exists():
        return Response({'error': 'Tato přezdívka je již používána jiným uživatelem'}, status=status.HTTP_400_BAD_REQUEST)
    
    hashed_passphrase = make_password(passphrase)

    student = Student.objects.create(username=username, passphrase=hashed_passphrase)
    student.save()

    return Response({'message': 'Student registered successfully!','id': student.id}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_student(request):
    username = request.data.get('username')
    passphrase = request.data.get('passphrase')

    # Check if username and passphrase are provided
    if not username or not passphrase:
        return Response({'error': 'Nebyly zadány všechny potřebné údaje'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if user exists
    try:
        student = Student.objects.get(username=username)
    except Student.DoesNotExist:
        return Response({'error': 'Nesprávné přihlašovací údaje'}, status=status.HTTP_400_BAD_REQUEST)

    # Check passphrase
    if check_password(passphrase, student.passphrase):
        return Response({'message': 'Login successful!','id': student.id, 'role': 'student'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Nesprávné přihlašovací údaje'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def login_admin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if username and passphrase are provided
    if not username or not password:
        return Response({'error': 'Nebyly zadány všechny potřebné údaje'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if user exists
    try:
        admin = Admin.objects.get(username=username)
    except Admin.DoesNotExist:
        return Response({'error': 'Nesprávné přihlašovací údaje'}, status=status.HTTP_400_BAD_REQUEST)

    # Check passphrase
    if check_password(password, admin.password):
        return Response({'message': 'Přihlášení proběhlo úspěšně!', 'role': 'admin'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Nesprávné přihlašovací údaje'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def check_answer(request):
    student_id = request.data.get('student_id')
    example_id = request.data.get('example_id')
    date = request.data.get('date')
    duration = request.data.get('duration')
    student_answer = request.data.get('student_answer')
    answer_type = request.data.get('answer_type')

    if not student_id or not example_id or not date or not duration or not answer_type:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    match answer_type:
        case "inline":
            isCorrect, continue_with_next = InlineAnswerChecker.verifyAnswer(student_id, example_id, date, duration, student_answer)
            pass

        case "fraction":
            isCorrect, continue_with_next = FractionAnswerChecker.verifyAnswer(student_id, example_id, date, duration, student_answer)
            pass

        case "variable":
            isCorrect, continue_with_next = VariableAnswerChecker.verifyAnswer(student_id, example_id, date, duration, student_answer)
            pass

        case _:
            return Response({'error': 'Invalid answer type'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'isCorrect': isCorrect, 'continue_with_next': continue_with_next}, status=status.HTTP_200_OK)    


from django.db.models import Sum
from django.db.models.functions import TruncMinute

@api_view(['GET'])
def attempts_over_time(request):
    try:
        # Get student_id from query params (adjust as needed)
        student_id = request.query_params.get('student_id')
        
        if not student_id:
            return Response({"error": "Missing student_id"}, status=status.HTTP_400_BAD_REQUEST)

        # Aggregate attempts per minute (or change to hour/day)
        data = (
            StudentExample.objects
            .filter(student_id=student_id)
            .annotate(time_group=TruncMinute('date'))
            .values('time_group')
            .annotate(total_attempts=Sum('attempts'))
            .order_by('time_group')
        )

        # Format data for ApexCharts
        response_data = {
            'categories': [item['time_group'].strftime('%H:%M') for item in data],
            'series': [
                {
                    'name': 'Attempts',
                    'data': [item['total_attempts'] for item in data]
                }
            ]
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.db.models import Avg, Count

@api_view(['GET'])
def average_duration(request):
    student_id = request.GET.get('student_id', 1)  # Default to student 1 if not provided

    # Aggregate data: Group by date and calculate the average duration
    data = (
        StudentExample.objects
        .filter(student_id=student_id)
        .values('date__date')  # Group by date only (without time)
        .annotate(avg_duration=Avg('duration'))  # Calculate average
        .order_by('date__date')  # Sort by date
    )

    # Convert queryset to list of dictionaries
    result = [
        {"date": item["date__date"].strftime("%Y-%m-%d"), "avg_duration": round(item["avg_duration"], 2)}
        for item in data
    ]

    return JsonResponse(result, safe=False)

from django.utils.timezone import make_aware
from datetime import datetime, timedelta

@api_view(['GET'])
def counted_examples(request):
    student_id = request.GET.get('student_id')
    if not student_id:
        return JsonResponse({"error": "Missing student_id"}, status=400)

    # Get the date range (from 20.2 to 28.2)
    start_date = make_aware(datetime(2025, 2, 20))
    end_date = make_aware(datetime(2025, 2, 28))

    # Query counted examples per day
    data = (
        StudentExample.objects.filter(student_id=student_id, date__date__range=[start_date, end_date])
        .values('date__date')  # Group by day only (ignore time)
        .annotate(example_count=Count('id'))
        .order_by('date__date')
    )

    # Format response
    response_data = [
        {"date": entry["date__date"].strftime("%Y-%m-%d"), "example_count": entry["example_count"]}
        for entry in data
    ]

    return JsonResponse(response_data, safe=False)

""""
@api_view(['POST'])
def transcribe_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_chunk'):
        # Get the uploaded audio file
        audio_chunk = request.FILES['audio_chunk']
        
        # Log the MIME type for debugging
        print("Received file format:", audio_chunk.content_type)

        # Define the path where the audio file will be saved
        audio_file_path = os.path.join(BASE_DIR, 'uploaded_audio.webm')
        
        try:
            # Save the audio file to the server
            with open(audio_file_path, 'wb') as f:
                for chunk in audio_chunk.chunks():
                    f.write(chunk)
            
            # Return a success response with the saved file's path
            return JsonResponse({'message': 'Audio file saved successfully', 'file_path': audio_file_path}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Error saving audio file: {str(e)}'}, status=400)

    else:
        return JsonResponse({'error': 'No audio file received'}, status=400)


@api_view(['POST'])
def transcribe_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_chunk'):
        audio_chunk = request.FILES['audio_chunk']
        print("Received file format:", audio_chunk.content_type) 

        # Use a BytesIO object to handle the file in memory instead of saving it to disk
        audio_file = BytesIO()
        for chunk in audio_chunk.chunks():
            audio_file.write(chunk)
        
        # Ensure the file pointer is at the start of the audio file before sending it
        audio_file.seek(0)

        try:
            # Send the audio file to OpenAI Whisper API for transcription
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )

            # Return the transcription text
            return JsonResponse({'transcription': transcription['text']}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'No audio file received'}, status=400)
"""
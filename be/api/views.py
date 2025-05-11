"""
================================================================================
 Module: views.py
 Description:
        Contains API views that serve the frontend with data manipulation functionality.
        It includes CRUD operations for tasks, examples, skills, and student records.
        It also handles user authentication and answer checking.

 Author: Dominik Horut (xhorut01)
================================================================================
"""

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.db import transaction
from .models import Task, Example, Answer, Student, Skill, ExampleSkill, StudentExample, Admin, Step
from .serializers import ExampleSerializer, SkillSerializer, RecordInitSerializer
from .utils import get_height, build_skill_tree, get_skill_paths, get_skill_names_string_sync
from .answerChecker import InlineAnswerChecker, FractionAnswerChecker, VariableAnswerChecker
import json
import random
from datetime import datetime
import os

# Add all skill_ids to the related_skills field of each skill
def create_skill_relations(skill_ids):

    skills = Skill.objects.filter(id__in=skill_ids)

    for skill in skills:
        related_skills = [s for s in skills if s != skill and s.skill_type != skill.skill_type]
        skill.related_skills.add(*related_skills)  

# Creates a new task and its examples
@api_view(['POST'])
def create_task(request):
    task_name = request.data.get('task_name')
    task_form = request.data.get('task_form')
    skill_ids = request.data.get('skill_ids', [])
    examples_data = request.data.get('examples', [])  

    if not task_name:
        return Response({"error": "Nebyl zadán název sady"}, status=status.HTTP_400_BAD_REQUEST)

    skills = Skill.objects.filter(id__in=skill_ids)

    if not skills.exists():
        return Response({"error": "Nebyly zadány žádné dovednosti"}, status=status.HTTP_400_BAD_REQUEST)

    task_instance, created = Task.objects.get_or_create(name=task_name)

    task_instance.form = task_form 

    task_instance.save()

    # Assign skills to the task
    task_instance.skills.add(*skills)

    created_examples = []

    # Loop through each example data and create it
    for example_data in examples_data:
        example_text = example_data.get('example')
        input_type = example_data.get('input_type')
        answer_text = example_data.get('answer')
        steps = example_data.get('steps', [])

        # Validate required fields
        if not example_text or not input_type:
            continue 

        
        example_payload = {
            'example': example_text,
            'input_type': input_type,
            'task': task_instance.id  
        }
        example_serializer = ExampleSerializer(data=example_payload)
        
        if example_serializer.is_valid():
            with transaction.atomic():  
                example_instance = example_serializer.save()

                # Create answer of example
                if answer_text:
                    Answer.objects.create(example=example_instance, answer=answer_text)

                # Assign skills to the example
                for skill in skills:
                    ExampleSkill.objects.create(example=example_instance, skill=skill)
                
                create_skill_relations(skill_ids)

                # Create example steps if any
                for index, step_text in enumerate(steps, start=1):
                    if step_text:  
                        Step.objects.create(
                            example=example_instance,
                            text=step_text,
                            order=index  
                        )

                
                created_examples.append(example_serializer.data)
    
    return Response({"created_examples": created_examples}, status=status.HTTP_201_CREATED)

# Edits an existing task and its examples
@api_view(['POST'])
def edit_task(request):
    task_id = request.data.get('task_id')
    task_name = request.data.get('task_name')
    task_form = request.data.get('task_form')   
    skill_ids = request.data.get('skill_ids', [])
    examples_data = request.data.get('examples', [])

    if not task_id:
        return Response({"error": "Nebyl zadán ID sady"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        task_instance = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    # Update task attributes
    if task_name:
        task_instance.name = task_name
        task_instance.form = task_form
        task_instance.save()

    skills = Skill.objects.filter(id__in=skill_ids)
    if not skills.exists():
        return Response({"error": "At least one valid skill ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Update tasks skills
    task_instance.skills.set(skills)

    updated_examples = []

    # Loop through each example in the request data
    for example_data in examples_data:
        example_id = example_data.get('example_id')
        example_text = example_data.get('example')
        input_type = example_data.get('input_type')
        answer_text = example_data.get('answer')
        steps = example_data.get('steps', [])

        if not example_text or not input_type:
            continue  

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

        # Update related skills to the example
        existing_relations = ExampleSkill.objects.filter(example=example_instance)
        new_skill_ids = set(skill.id for skill in skills)
        existing_relations.exclude(skill_id__in=new_skill_ids).delete()

        for skill in skills:
            ExampleSkill.objects.update_or_create(example=example_instance, skill=skill)
        
        create_skill_relations(skill_ids)

        # Update or create Step instances
        Step.objects.filter(example=example_instance).delete() 
        for index, step_text in enumerate(steps, start=1):
            if step_text:
                Step.objects.create(
                    example=example_instance,
                    order=index,
                    text=step_text
                )

        example_serializer = ExampleSerializer(example_instance)
        updated_examples.append(example_serializer.data)

    
    return Response({"updated_examples": updated_examples}, status=status.HTTP_200_OK)

# Get skill data by provided skill id
@api_view(['GET'])
def get_skill(request, skill_id):
    try:
        skill = Skill.objects.get(id=skill_id)

        if skill.deleted == True:
            return Response({"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)
        
        skill_data = SkillSerializer(skill).data
    
        return Response(skill_data, status=status.HTTP_200_OK)

    except Skill.DoesNotExist:
        return Response({"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

# Get all examples for the provided skill ids
@api_view(['GET'])
def get_examples(request):

    skills = request.query_params.get('topics')
    
    if not skills:
        return Response({"error": "No topics provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        skills_data = json.loads(skills)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format for topics"}, status=status.HTTP_400_BAD_REQUEST)

    # Get skill paths to get examples containing them
    skill_paths = get_skill_paths(skills_data)

    example_data = []

    for path in skill_paths:

        examples = Example.objects.filter(
            exampleskill__skill__id__in=path
        ).distinct()

        for example in examples:

            example_skill_ids = set(example.exampleskill_set.values_list('skill__id', flat=True))

            # Check if the example skill ids contain all the skills in the current path (no missing skills)
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

# Create a new record that user practiced the example
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
        response_data['date'] = record.date

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(record_init_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Updates record that user practiced the example
@api_view(['POST'])
def update_example_record(request):
    # Data to identify the record
    student = request.data.get('student_id')
    example = request.data.get('example_id')
    date = request.data.get('date')

    # Duration how long it took user to enter the answer
    duration = request.data.get('time')
  
    if not student or not example or not duration:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    student_example = get_object_or_404(StudentExample, student_id=student, example_id=example, date=date)
    
    try:
        with transaction.atomic():
            # Update record data
            student_example.attempts += 1
            student_example.duration = duration

            # Determine if limit of tries is reached and new example should be shown to user
            next_example = student_example.attempts == 3
                         
            student_example.save()
        
        return Response({"message": "Record updated successfully", "next_example": next_example}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Deletes record that user practiced the example        
@api_view(['POST'])
def delete_example_record(request):
    # Data to identify the record
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

# Updates example record to skipped
@api_view(['POST'])
def skip_example(request):
    # Data to identify the record
    student = request.data.get('student_id')
    example = request.data.get('example_id')
    date = request.data.get('date')

    if not student or not example or not date:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    student_example = get_object_or_404(StudentExample, student_id=student, example_id=example, date=date)

    try:
        with transaction.atomic():

            # Record is marked as skipped and attempts and duration are not relevant
            student_example.skipped = True
            student_example.attempts = 0
            student_example.duration = 0
                        
            student_example.save()
        
        return Response({"message": "Example skipped"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get all tasks and their examples
@api_view(['GET'])
def get_tasks(request):
    tasks = Task.objects.prefetch_related(
        'example_set__answers',         
        'example_set__exampleskill_set__skill', 
        'example_set__steps'           
    )
    
    data = []
    for task in tasks:
        # Get skills for the task
        skills = []
        # Use the first example to get skills, since all examples share the same skills
        first_example = task.example_set.first()
        if first_example:
            skills = [
                {
                    "id": example_skill.skill.id,
                    "name": example_skill.skill.name,
                    "height": example_skill.skill.height,
                    "skill_type": example_skill.skill.skill_type,
                    "parent_skill": example_skill.skill.parent_skill.id if example_skill.skill.parent_skill else None,
                    "related_skills": list(example_skill.skill.related_skills.values_list('id', flat=True))
                }
                for example_skill in first_example.exampleskill_set.all()
            ]
        
        # Get task data
        task_data = {
            "task_id": task.id,
            "task_name": task.name,
            "task_form": task.form,
            "skills": skills,  
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
        data.append(task_data)
    
    return JsonResponse(data, safe=False)

# Delete an example and its related data (answers, steps)
@api_view(['DELETE'])
def delete_example(request, example_id):
    example = get_object_or_404(Example, id=example_id)
    
    try:
        with transaction.atomic():
            example.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete a task and its related data
@api_view(['DELETE'])
def delete_task(request, task_id):
    try:
        with transaction.atomic():
            task = get_object_or_404(Task, id=task_id)
            
            related_skills = list(task.skills.all())  

            # Remove connections from the skill-task relationship
            task.skills.clear()

            # Delete the task and its related data (examples, answers, steps)
            task.delete()

            # Check skill relationships and remove them if no other task uses them
            for skill in related_skills:
                for related_skill in skill.related_skills.all():
                    # Get all tasks where both skills are used together
                    shared_tasks = Task.objects.filter(skills=skill).filter(skills=related_skill)
                    
                    # If this was the last task using this relationship, remove the relation
                    if not shared_tasks.exists():
                        skill.related_skills.remove(related_skill)
                        related_skill.related_skills.remove(skill)

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response(
            {"error": f"Error deleting task: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

# Create a new skill or restore a deleted one
@api_view(['POST'])
def create_skill(request):
    try:
        name = request.data.get('name')
        parent_skill_id = request.data.get('parent_skill')

        if not name:
            return Response({"error": "Skill name is required."}, status=status.HTTP_400_BAD_REQUEST)

        parent_skill = None
        skill_type = None

        # Prepare new skill data
        if parent_skill_id:
            parent_skill = get_object_or_404(Skill, id=parent_skill_id)
            skill_type = parent_skill.skill_type  
            height = get_height(parent_skill_id) + 1
        
        # No parent skill
        else:
            height = 0  
        # Check if a skill with the same name already exists and is not deleted
        existing_skill = Skill.objects.filter(name=name, deleted=True).first()
        
        if existing_skill:
            # If a deleted skill exists with the same name, restore it
            existing_skill.deleted = False
            existing_skill.save()

            return JsonResponse({
                "id": existing_skill.id,
                "name": existing_skill.name,
                "parent_skill": existing_skill.parent_skill.id if existing_skill.parent_skill else None,
                "skill_type": existing_skill.skill_type,  
            }, status=status.HTTP_200_OK)

        # If no deleted skill exists, create a new skill
        else:
            with transaction.atomic():  
                skill = Skill.objects.create(
                    name=name, 
                    parent_skill=parent_skill, 
                    skill_type=skill_type, 
                    height=height
                )

            return JsonResponse({
                "id": skill.id,
                "name": skill.name,
                "parent_skill": skill.parent_skill.id if skill.parent_skill else None,
                "skill_type": skill.skill_type, 
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get all skills in a tree structure
@api_view(['GET'])
def get_skill_tree(request):
    skills = Skill.objects.filter(deleted=False)
    skill_list = SkillSerializer(skills, many=True).data

    # Convert the flat list into a hierarchical structure
    skill_dict = {skill["id"]: {**skill, "children": []} for skill in skill_list}

    root_skills = []

    # Build the tree structure
    for skill in skill_dict.values():

        if skill["parent_skill"] is None:
            root_skills.append(skill)

        else:
            parent = skill_dict.get(skill["parent_skill"])
            if parent:
                parent["children"].append(skill)

    return Response(root_skills)

# Search for skills based on a query and parent skill
@api_view(['GET'])
def search_skills(request):
    query = request.GET.get('q', '') 
    skill_id = request.GET.get('skill_id', None) 

    if not skill_id:
        return Response([]) 

    try:
        parent_skill = Skill.objects.get(id=skill_id)

    except Skill.DoesNotExist:
        return Response([])

    if query:
        # Searched skill name must be children of provided parent skill
        skills = Skill.objects.filter(
            name__icontains=query, 
            parent_skill=parent_skill,
            deleted=False  
        )
    # No query provided, get all children of the parent skill   
    else:
        skills = Skill.objects.filter(parent_skill=parent_skill, deleted=False)

    skill_list = SkillSerializer(skills, many=True).data

    return Response(skill_list)

# Get skills which should be displayed on landing page
@api_view(['GET'])
def get_landing_page_skills(request):

    # Get non-deleted skills
    existing_skills = Skill.objects.filter(deleted=False)

    # Filter skills that should not be displayed (height <= 3)
    skills_with_height = existing_skills.filter(height__lte=3)

    # Get leaf skills
    leaf_skills = skills_with_height.filter(subskills__isnull=True)

    # Get skills with height 3
    skills_with_height_3 = existing_skills.filter(height=3)

    # Displayed skills should be leaf skills or have height == 3    
    skills = (leaf_skills | skills_with_height_3).distinct()

    serializer = SkillSerializer(skills, many=True)

    return Response(serializer.data)

# Get all skills related to the selected skill  
@api_view(['GET'])
def get_related_skills_tree(request, skill_id):
    try:
        main_skill = Skill.objects.get(id=skill_id, deleted=False)  
        visited = set()
        tree = []

        related_skills = main_skill.related_skills.filter(deleted=False)    

        # Build tree structure to be visualized in the frontend
        for skill in related_skills:
            skill_ids = [main_skill.id, skill.id] 
            if skill.id not in visited:
                subtree = build_skill_tree(skill, visited, skill_ids, related_skills, None)
                if subtree:
                    tree.append(subtree)

        return Response(tree)

    except Skill.DoesNotExist:
        return Response({"error": "Skill not found"}, status=404)

# Get all children skills of the selected skill
@api_view(['GET'])
def get_children_skills_tree(request, skill_id):

    # Edge case for Equation skills
    withCounts = request.GET.get('with_counts', 'false') == 'true'

    try:
        main_skill = Skill.objects.get(id=skill_id)  

        if main_skill.deleted:
            return Response({"error": "Skill not found"}, status=404)   
        visited = set()  
        tree = []
        
        # Get all children skills of the selected skill
        children = Skill.objects.filter(parent_skill=main_skill, deleted=False)

        # Build subtree structure of each child to be visualized in the frontend
        for skill in children:
            if skill.id not in visited:
                subtree = build_skill_tree(skill, visited, None, None, withCounts) 
                if subtree:
                    tree.append(subtree)

        return Response(tree)  

    except Skill.DoesNotExist:
        return Response({"error": "Skill not found"}, status=404)

# Get all operation skills related to the selected skill    
@api_view(['GET'])
def get_operation_skills(request, skill_id):
    try:
        main_skill = get_object_or_404(Skill, id=skill_id)

        if main_skill.deleted:
            return Response({"error": "Skill not found"}, status=404)

        # Get all children skills of the selected skill
        children_skills = main_skill.subskills.filter(deleted=False)

        # Get all operation skills related to the selected skill    
        related_operation_skills = main_skill.related_skills.filter(skill_type='OPERATION', deleted=False)

        skills_data = []

        for operation_skill in related_operation_skills:
            child_data = []

            for child_skill in children_skills:
                # Count examples that have both operation_skill and child_skill
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

            # Include only single operations not parent skill Operations
            if operation_skill.height >= 3:
                skills_data.append({
                "id": operation_skill.id,
                "name": operation_skill.name,
                "related_skills": child_data
                })

        return Response(skills_data)
    
    except Skill.DoesNotExist:
        return Response({"error": "Skill not found"}, status=404)

# Soft delete a skill and remove all its relations
@api_view(['PATCH'])
def delete_skill(request, skill_id):
    try:
        skill = Skill.objects.get(id=skill_id)
        
        # Mark the skill as deleted
        skill.deleted = True
        skill.save()
        
        # Remove this skill from all related examples
        ExampleSkill.objects.filter(skill=skill).delete()
        
        # Remove this skill from realtions with tasks
        for task in Task.objects.filter(skills=skill):
            task.skills.remove(skill)
        
        # Remove this skill from all related_skills
        for related_skill in skill.related_skills.all():
            skill.related_skills.remove(related_skill)
        
        return Response(
            {"message": f"Skill '{skill.name}' marked as deleted and all relations removed."},
            status=status.HTTP_200_OK
        )
        
    except Skill.DoesNotExist:
        return Response(
            {"error": "Skill not found."},
            status=404
        )

# Create new user account
@api_view(['POST'])
def register_student(request):
    username = request.data.get('username')
    passphrase = request.data.get('passphrase')

    if not username or not passphrase:
        return Response({'error': 'Chybí uživatelské jméno nebo heslo'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Student.objects.filter(username=username).exists():
        return Response({'error': 'Tato přezdívka je již používána jiným uživatelem'}, status=status.HTTP_400_BAD_REQUEST)
    
    hashed_passphrase = make_password(passphrase)

    student = Student.objects.create(username=username, passphrase=hashed_passphrase)
    student.save()

    return Response({'message': 'Student registered successfully!','id': student.id}, status=status.HTTP_201_CREATED)

# Login user account
@api_view(['POST'])
def login_student(request):
    username = request.data.get('username')
    passphrase = request.data.get('passphrase')

    if not username or not passphrase:
        return Response({'error': 'Nebyly zadány všechny potřebné údaje'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        student = Student.objects.get(username=username)
    except Student.DoesNotExist:
        return Response({'error': 'Nesprávné přihlašovací údaje'}, status=status.HTTP_400_BAD_REQUEST)

    if check_password(passphrase, student.passphrase):
        return Response({'message': 'Login successful!','id': student.id, 'role': 'student'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Nesprávné přihlašovací údaje'}, status=status.HTTP_401_UNAUTHORIZED)
    
# Login admin account   
@api_view(['POST'])
def login_admin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Nebyly zadány všechny potřebné údaje'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        admin = Admin.objects.get(username=username)
    except Admin.DoesNotExist:
        return Response({'error': 'Nesprávné přihlašovací údaje'}, status=status.HTTP_400_BAD_REQUEST)

    if check_password(password, admin.password):
        return Response({'message': 'Přihlášení proběhlo úspěšně!', 'role': 'admin'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Nesprávné přihlašovací údaje'}, status=status.HTTP_401_UNAUTHORIZED)

# Check if the keyboard entered answer is correct
@api_view(['POST'])
def check_answer(request):

    student_id = request.data.get('student_id')
    example_id = request.data.get('example_id')

    # Data for record creation
    date = request.data.get('date')
    duration = request.data.get('duration')

    student_answer = request.data.get('student_answer')
    answer_type = request.data.get('answer_type')

    if not student_id or not example_id or not date or not duration or not answer_type:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Choose the answer checker based on the answer type
    match answer_type:
        case "inline" | "word":
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
    
    # Return if answer was corrrect and if new example should be shown
    return Response({'isCorrect': isCorrect, 'continue_with_next': continue_with_next}, status=status.HTTP_200_OK)    

# Get all skill paths from skill ids to be displayed when editing task
@api_view(['GET'])
def get_paths_for_sandbox(request):
    skill_ids = request.GET.getlist('skill_ids', [])  

    if len(skill_ids) == 1 and ',' in skill_ids[0]:
        skill_ids = skill_ids[0].split(',')

    try:
        skill_ids = [int(id) for id in skill_ids] 
        skill_paths = get_skill_paths(skill_ids, False)
        return Response(skill_paths, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get number of tasks and examples related to the selected skill
@api_view(['GET'])
def get_skill_related_counts(request):
    skill_id = request.GET.get('skill_id')

    skill = get_object_or_404(Skill, id=skill_id)

    task_count = Task.objects.filter(skills=skill).count()

    example_count = ExampleSkill.objects.filter(skill=skill).count()

    data = {
        "task_count": task_count,
        "example_count": example_count
    }

    return Response(data)

# Directory to save survey answers  
SURVEY_DIR = "survey"
os.makedirs(SURVEY_DIR, exist_ok=True)

# Save survey answer to a JSON file
@api_view(['POST'])
def save_survey_answer(request):

    # Survey answer data
    question_type = request.data.get('question_type')
    question_text = request.data.get('question_text')
    answer = request.data.get('answer')
    skills = request.data.get('skills')

    # Skills which were practiced when question was asked
    skill_names = get_skill_names_string_sync(skills)

    if not question_type or not question_text or not answer:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    json_filename = f"{question_type}_{timestamp}.json"
    json_filepath = os.path.join(SURVEY_DIR, json_filename)
        
    survey_question_data = {
        "question_text": question_text,
        "answer": answer,
        "examples_type": skill_names,
        "timestamp": timestamp
    }

    # Save the survey answer to a JSON file
    with open(json_filepath, "w", encoding="utf-8") as json_file:
        json.dump(survey_question_data, json_file, indent=4, ensure_ascii=False)
    
    return Response(status=status.HTTP_200_OK)
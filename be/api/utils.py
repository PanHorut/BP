"""
================================================================================
 Module: utils.py
 Description: 
        Implements utility functions mostly for working with skill tree
 Author: Dominik Horut (xhorut01)
================================================================================
"""

from .models import Skill, ExampleSkill
from collections import defaultdict
from datetime import datetime, timezone
from asgiref.sync import sync_to_async

# Get the height of a skill in the skill tree
def get_height(id):
    
    skill = Skill.objects.get(id=id)
    
    distance = 0
    while skill.parent_skill:  
        skill = skill.parent_skill
        distance += 1
    return distance

# Return the count of examples that have all the skills provided in skill_ids
def examples_with_skills(skill_ids):
    
    try:
        if not skill_ids:
            return 0
            
        skill_ids_set = set(skill_ids)
        
        example_skills = ExampleSkill.objects.filter(skill__in=skill_ids).values('example', 'skill')
        
        # Group skills by example
        example_to_skills = {}
        for item in example_skills:
            example_id = item['example']
            skill_id = item['skill']
            
            if example_id not in example_to_skills:
                example_to_skills[example_id] = set()
            example_to_skills[example_id].add(skill_id)
        
        # Count examples that have all required skills
        valid_count = sum(1 for skills in example_to_skills.values() 
                         if skill_ids_set.issubset(skills))
                         
        return valid_count

    except Skill.DoesNotExist:
        return 0

# Build a tree of skills starting from the given skill
def build_skill_tree(skill, visited=None, skill_ids=None, related_skills=None, withCounts=None):
    if visited is None:
        visited = set()

    if related_skills is None:
        related_skills = set()
    
    # Avoid infinite loops
    if skill.id in visited:
        return None  
    
    visited.add(skill.id)

    children = Skill.objects.filter(parent_skill=skill)

    if skill_ids is None:
        skill_ids = [skill.id]
    else:
        skill_ids.append(skill.id)

    examples_count = 0

    print("With count", withCounts)
    print("Skill ids", skill_ids)
    if related_skills and skill in related_skills:
        examples_count = examples_with_skills(skill_ids)
    
    # Edge case for Equations which are not related to Operations
    if withCounts:
        examples_count = examples_with_skills(skill_ids)
    
    
    # Skip general skills like Operations or Number Domains
    if skill.height >= 3:
        return {
        "id": skill.id,
        "name": skill.name,
        "examples": examples_count,
        "subskills": [
            build_skill_tree(child, visited, skill_ids.copy(), related_skills)
            for child in children if related_skills and child in related_skills
        ]
        }

# Create skill paths for given skill ids based on skill tree
def get_skill_paths(skill_ids, merge=True):

    skills = Skill.objects.filter(id__in=skill_ids).select_related('parent_skill')
    
    skill_dict = {skill.id: skill for skill in skills}
    
    parent_map = defaultdict(list)
    for skill in skills:
        if skill.parent_skill_id:
            parent_map[skill.parent_skill_id].append(skill.id)
    
    paths = []
    visited = set()
    
    # Build paths from a given skill
    def build_paths(skill_id, current_path):
        if skill_id in visited:
            return
        visited.add(skill_id)
        
        new_path = current_path + [skill_id]
        children = parent_map.get(skill_id, [])

        if children:
            for child in children:
                build_paths(child, new_path)
        else:
            paths.append(new_path)

    # Identify root skills (no parent or parent not in selected skills)
    root_skills = [skill.id for skill in skills if not skill.parent_skill_id or skill.parent_skill_id not in skill_dict]

    # Build paths starting from each root
    for root in root_skills:
        build_paths(root, [])

    # Merge overlapping paths into unique paths
    if merge:       
        return merge_unique_lists(paths)
    else:
        return paths

# Merge created skill paths unless they contain sibling skills (same parent)
def merge_unique_lists(input_lists):
    result = []

    # Check if two skills share the same parent
    def are_siblings(skill1, skill2):
        return skill1.parent_skill == skill2.parent_skill
    
    if(len(input_lists) == 1):
        return input_lists
    
    for i in range(len(input_lists)):
        
        for j in range(i + 1, len(input_lists)):

            list_i_skills = [Skill.objects.get(id=skill_id) for skill_id in input_lists[i]]
            list_j_skills = [Skill.objects.get(id=skill_id) for skill_id in input_lists[j]]
            
            # If no sibling skills between the two lists, merge them    
            if not any(are_siblings(skill1, skill2) for skill1 in list_i_skills for skill2 in list_j_skills):
                result.append(input_lists[i] + input_lists[j])

    return result

# Calculate the duration in milliseconds from the record date to now
def calculate_duration(record_date_str):
   
    if not record_date_str:
        return 0  

    try:
        record_date = datetime.strptime(record_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        record_date = record_date.replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)

        return int((current_time - record_date).total_seconds() * 1000)
    
    except ValueError as e:
        print(f"Error parsing record_date: {e}")
        return 0  

# Extract only skill names from the skills data
def get_skill_names_string_sync(skill_ids):
    
    if not skill_ids:
        return ""
    
    skills = Skill.objects.filter(id__in=skill_ids, deleted=False)
    
    skill_names = [skill.name for skill in skills]
    
    return ", ".join(skill_names)

# Async version used in websocket communication
get_skill_names_string = sync_to_async(get_skill_names_string_sync)


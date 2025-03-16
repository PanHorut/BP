from .models import Skill, ExampleSkill
from collections import defaultdict
from datetime import datetime, timezone



# gets the height of a node in a tree of skills
def get_height(id):
    skill = Skill.objects.get(id=id)
    
    distance = 0
    while skill.parent_skill:  
        skill = skill.parent_skill
        distance += 1
    return distance

# retuns the number of examples that have all the skills in the list
def examples_with_skills(skill_ids):

    try:
        skills = Skill.objects.filter(id__in=skill_ids)
        
        examples = ExampleSkill.objects.filter(skill__in=skills).values('example').distinct()
        
        valid_examples = []

        for example in examples:
            example_id = example['example']
            linked_skills = ExampleSkill.objects.filter(example_id=example_id).values_list('skill', flat=True)

            if set(skill_ids).issubset(linked_skills):
                valid_examples.append(example_id)

        return len(valid_examples)

    except Skill.DoesNotExist:
        return 0

# build skill tree for a given skill 
def build_skill_tree(skill, visited=None, skill_ids=None, related_skills=None, withCounts=None):
    if visited is None:
        visited = set()

    if related_skills is None:
        related_skills = set()
    
    # to avoid infinite loops
    if skill.id in visited:
        return None  
    
    visited.add(skill.id)

    children = Skill.objects.filter(parent_skill=skill)

    if skill_ids is None:
        skill_ids = [skill.id]
    else:
        skill_ids.append(skill.id)

    examples_count = 0
    if related_skills and skill in related_skills:
        examples_count = examples_with_skills(skill_ids)

    if withCounts:
        examples_count = examples_with_skills(skill_ids)
    
    
    # nechci obecne skilly jako Operace nebo Číselné obory
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


# get skill paths from skill list 
def get_skill_paths(skill_ids, merge=True):
    skills = Skill.objects.filter(id__in=skill_ids).select_related('parent_skill')
    
    skill_dict = {skill.id: skill for skill in skills}
    
    parent_map = defaultdict(list)
    for skill in skills:
        if skill.parent_skill_id:
            parent_map[skill.parent_skill_id].append(skill.id)
    
    paths = []
    visited = set()
    
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
    
    root_skills = [skill.id for skill in skills if not skill.parent_skill_id or skill.parent_skill_id not in skill_dict]

    for root in root_skills:
        build_paths(root, [])

    if merge:       
        return merge_unique_lists(paths)
    else:
        return paths

# merge created skill paths with unrelated skills 
def merge_unique_lists(input_lists):
    result = []
    def are_siblings(skill1, skill2):
        return skill1.parent_skill == skill2.parent_skill
    
    if(len(input_lists) == 1):
        return input_lists
    
    for i in range(len(input_lists)):
        
        for j in range(i + 1, len(input_lists)):

            list_i_skills = [Skill.objects.get(id=skill_id) for skill_id in input_lists[i]]
            list_j_skills = [Skill.objects.get(id=skill_id) for skill_id in input_lists[j]]
            
            # check if there's any sibling relationship between the two lists and avoid merging them    
            if not any(are_siblings(skill1, skill2) for skill1 in list_i_skills for skill2 in list_j_skills):
                result.append(input_lists[i] + input_lists[j])

    return result


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






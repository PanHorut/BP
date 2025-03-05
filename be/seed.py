import os
import django
from django.contrib.auth.hashers import make_password  # Import password hashing

# Step 1: Set DJANGO_SETTINGS_MODULE before any Django imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")

# Step 2: Initialize Django settings
django.setup()

from api.models import Admin, Skill  # Assuming your Admin model is in the 'api' app
from api.answerChecker import AnswerChecker, InlineAnswerChecker, FractionAnswerChecker, VariableAnswerChecker    
from api.utils import get_skill_paths



if __name__ == "__main__":
    # Create the admin user
    #username = "admin1"
    #password = "kockanenipes"
        
    # Create and save the admin user
    #admin = Admin(username=username, password=password)
    #admin.save()
    
    #print(f"Admin user '{username}' created successfully!")
    answers = ["21"]
    #print(FractionAnswerChecker.verifyAnswer(10, 57, "2025-02-12 19:27:58.753704", 10, answers))   
    print(get_skill_paths([55, 56, 61, 67, 69], False))

  
    

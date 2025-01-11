import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")
django.setup()

from api.models import Skill

def seed_data():


    Skill.objects.create(name="Mocniny a odmocniny")
    Skill.objects.create(name="Výrazy")
    Skill.objects.create(name="Procenta")

    
    

if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully.")

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")
django.setup()

from api.models import Skill

def seed_data():
    Skill.objects.create(name="Sčítání a odčítání desetinných čísel")
    Skill.objects.create(name="Násobení a dělení desetinných čísel")
    Skill.objects.create(name="Desetinná čísla")
    

if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully.")

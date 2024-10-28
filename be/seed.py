import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")
django.setup()

from api.models import Skill

def seed_data():
    # Create the main skill
    fractions_skill = Skill.objects.create(name="Zlomky")

    # Create the dependent skills with `parent_skill` set to `fractions_skill`
    Skill.objects.create(name="Sčítání a odčítání zlomků", parent_skill=fractions_skill)
    Skill.objects.create(name="Násobení a dělení zlomků", parent_skill=fractions_skill)
    

if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully.")

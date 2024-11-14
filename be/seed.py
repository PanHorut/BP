import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be.settings")
django.setup()

from api.models import Skill

def seed_data():
    # Decimal skill
    parent1 = Skill.objects.create(name="Desetinná čísla")

    Skill.objects.create(name="Sčítání a odčítání desetinných čísel", parent_skill=parent1)
    Skill.objects.create(name="Násobení a dělení desetinných čísel", parent_skill=parent1)

    # Equations
    parent2 = Skill.objects.create(name="Rovnice")

    Skill.objects.create(name="Lineární rovnice s jednou neznámou", parent_skill=parent2)

    # ne equations
    parent3 = Skill.objects.create(name="Nerovnice")

    Skill.objects.create(name="Lineární nerovnice", parent_skill=parent3)
    
    # fractions
    parent4 = Skill.objects.create(name="Zlomky")

    Skill.objects.create(name="Sčítání a odčítání zlomků", parent_skill=parent4)
    Skill.objects.create(name="Násobení zlomků", parent_skill=parent4)
    Skill.objects.create(name="Dělení zlomků", parent_skill=parent4)

     # lomene
    parent5 = Skill.objects.create(name="Lomené výrazy")

    Skill.objects.create(name="Krácení lomených výrazů", parent_skill=parent5)
    Skill.objects.create(name="Sčítání a odčítání lomených výrazů", parent_skill=parent5)
    Skill.objects.create(name="Násobení lomených výrazů", parent_skill=parent5)
    Skill.objects.create(name="Dělení lomených výrazů", parent_skill=parent5)

    

    
    

if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully.")

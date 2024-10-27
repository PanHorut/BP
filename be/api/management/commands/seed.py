from django.core.management.base import BaseCommand
from api.models import Skill 

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Create example data
        Skill.objects.create(name='add-sub')
        Skill.objects.create(name='mult-div')
        Skill.objects.create(name='frac')
        

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
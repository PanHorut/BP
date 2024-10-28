from django.db import models

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=255)

class Example(models.Model):
    example = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    input_type = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class Skill(models.Model):
    name = models.CharField(max_length=255)
    parent_skill = models.ForeignKey(
        'self',                  
        null=True,               
        blank=True,              
        on_delete=models.SET_NULL,
        related_name='dependent_skills'
    )
    
class ExampleSkill(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)



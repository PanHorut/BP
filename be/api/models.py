from django.db import models
from datetime import timedelta

class Task(models.Model):
    name = models.CharField(max_length=255)

class Example(models.Model):
    example = models.CharField(max_length=255)
    input_type = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class Answer(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=255)

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

class Student(models.Model):
    username = models.CharField(max_length=255)
    passphrase = models.CharField(max_length=255)

class StudentExample(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    example = models.ForeignKey(Example, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=0)
    attempts = models.IntegerField(default=1) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'example', 'date'], name='unique_student_example_date')
        ]


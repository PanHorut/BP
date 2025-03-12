from django.db import models
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password


class Task(models.Model):

    FORM_CHOICES = [
        ('classic', 'Classic'),
        ('word-problem', 'Word Problem'),
    ]

    name = models.CharField(max_length=255)
    skills = models.ManyToManyField(
        'Skill',  
        blank=True,  
        related_name='tasks' 
    )
    form = models.CharField(
        max_length=20, 
        choices=FORM_CHOICES, 
        default='classic', 
    )

class Example(models.Model):
    example = models.CharField(max_length=255)
    input_type = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class Step(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='steps')
    text = models.TextField()
    order = models.PositiveIntegerField(
        default=0,
    )

class Answer(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=255)

class Skill(models.Model):
    name = models.CharField(max_length=255)
    height = models.IntegerField(default=0) 
    parent_skill = models.ForeignKey(
        'self',                  
        null=True,               
        blank=True,              
        on_delete=models.SET_NULL,
        related_name='subskills'
    )

    SKILL_TYPES = [
        ('OPERATION', 'Operation'),
        ('NUMBER_DOMAIN', 'Number Domain'),
    ]
    
    skill_type = models.CharField(
        max_length=50, 
        choices=SKILL_TYPES, 
        null=True,               
        blank=True   
    )

    related_skills = models.ManyToManyField(
        'self',  
        blank=True,  
        symmetrical=True,  
    )
    
class ExampleSkill(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

class Student(models.Model):
    username = models.CharField(max_length=255,unique=True)
    passphrase = models.CharField(max_length=255)

class StudentExample(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    example = models.ForeignKey(Example, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0) 
    solved = models.BooleanField(default=False)
    skipped = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'example', 'date'], name='unique_student_example_date')
        ]

class Admin(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.pk is None: 
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, password):
        return check_password(password, self.password)

    def __str__(self):
        return self.username

class AudioPrompt(models.Model):
    audio_data = models.BinaryField()
    transcription = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    example = models.ForeignKey(Example, on_delete=models.CASCADE, null=True, blank=True)
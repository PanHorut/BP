# api/serializers.py
from rest_framework import serializers
from .models import Example
from .models import Skill
from .models import ExampleSkill
from .models import Task
from .models import Answer


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__' 

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__' 

class ExampleSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleSkill
        fields = ['example', 'skill']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__' 

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__' 
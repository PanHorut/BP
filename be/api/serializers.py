# api/serializers.py
from rest_framework import serializers
from . import models


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Example
        fields = '__all__' 

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Skill
        fields = '__all__' 

class ExampleSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExampleSkill
        fields = ['example', 'skill']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__' 

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__' 

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = '__all__'

class RecordInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentExample
        fields = ['student', 'example']


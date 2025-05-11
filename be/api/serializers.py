"""
================================================================================
 Module: serializers.py
 Description: 
        Defines serializers for converting model instances to and from JSON format
 Author: Dominik Horut (xhorut01)
================================================================================
"""

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

class RecordInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentExample
        fields = ['student', 'example']


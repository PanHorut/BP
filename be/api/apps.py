"""
================================================================================
 Module: apps.py
 Description: Configuration class for the Django application.
 Author: Dominik Horut (xhorut01)
================================================================================
"""

from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

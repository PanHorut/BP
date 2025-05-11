"""
================================================================================
 Module: urls.py
 Description: 
        Defines URL routing for HTTP views and WebSocket consumers in the app.
 Author: Dominik Horut (xhorut01)
================================================================================
"""

from django.urls import path
from . import views 
from .consumers import SpeechRecognitionConsumer
from .consumersSurvey import SurveySpeechTranscriptionConsumer

urlpatterns = [

    path('tasks/', views.get_tasks, name='get-tasks'),
    path('create-task/', views.create_task, name='create-task'),
    path('edit-task/', views.edit_task, name='edit-task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    
    path('examples/', views.get_examples, name='get-examples'),
    path('example/<int:example_id>/delete/', views.delete_example, name='delete_example'),

    path('create-record/', views.create_example_record, name='create-example-record'),
    path('update-record/', views.update_example_record, name='update-example-record'),
    path('delete-record/', views.delete_example_record, name='delete-example-record'),
    path('skip-example/', views.skip_example, name='skip-example'),
    path('check-answer/', views.check_answer, name='check-answer'),


    path('create-skill/', views.create_skill, name='create_skill'),
    path('skills/<int:skill_id>/delete/', views.delete_skill, name='delete-skill'),
    path('skill/<int:skill_id>/', views.get_skill, name='get-skill'),
    
    path('skill-tree/', views.get_skill_tree, name='get-skill-tree'),
    path('landing-page-skills/', views.get_landing_page_skills, name='get-landing-page-skills'),
    path('skills/<int:skill_id>/tree/related', views.get_related_skills_tree, name='related_skills_tree'),
    path('skills/<int:skill_id>/tree/children', views.get_children_skills_tree, name='children_skills_tree'),
    path('skills/<int:skill_id>/operations', views.get_operation_skills, name='operation_skills'),
    
    path('skills/search/', views.search_skills, name='skill-search'),
    path('skills/paths/sandbox/', views.get_paths_for_sandbox, name='get-sandbox-paths'),
    path('skills/related-counts/', views.get_skill_related_counts, name='get-skill-related-counts'),

    path('register/student', views.register_student, name='register_student'),
    path('login/student', views.login_student, name='login_student'),
    path('login/admin', views.login_admin, name='login_admin'),

    path('survey-answer/', views.save_survey_answer, name='save-survey-answer'),   
 
]

websocket_urlpatterns = [

    path('ws/speech/', SpeechRecognitionConsumer.as_asgi()),
    path('ws/survey/', SurveySpeechTranscriptionConsumer.as_asgi()),

]

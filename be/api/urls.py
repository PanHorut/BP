from django.urls import path
from . import views 
from .consumers import SpeechRecognitionConsumer

urlpatterns = [
    path('create-task/', views.create_task, name='create-task'),
    path('edit-task/', views.edit_task, name='edit-task'),

    path('skills/', views.SkillList.as_view(), name='skill-list'),
    path('skills/<int:skill_id>/delete/', views.delete_skill, name='delete-skill'),

    path('get-all-skills/', views.get_all_skills, name='get-all-skills'),
    path('examples-skills/', views.ExampleSkillList.as_view(), name='example-skill-list'),
    path('parent-skills/', views.get_parent_skills, name='get-parent-skills'),
    path('leaf-skills/', views.get_leaf_skills, name='get-leaf-skills'),

    path('skill/<int:skill_id>/', views.get_skill, name='get-skill'),
    path('examples/', views.get_examples, name='get-examples'),
    path('create-record/', views.create_example_record, name='create-example-record'),
    path('update-record/', views.update_example_record, name='update-example-record'),
    path('delete-record/', views.delete_example_record, name='delete-example-record'),
    path('skip-example/', views.skip_example, name='skip-example'),
    

    path('tasks/', views.get_tasks, name='get-tasks'),
    path('example/<int:example_id>/delete/', views.delete_example, name='delete_example'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('create-skill/', views.create_skill, name='create_skill'),
    path('skill-tree/', views.get_skill_tree, name='get-skill-tree'),
    path('skills/search/', views.search_skills, name='skill-search'),
    path('landing-page-skills/', views.get_landing_page_skills, name='get-landing-page-skills'),
    path('skills/<int:skill_id>/tree/related', views.get_related_skills_tree, name='related_skills_tree'),
    path('skills/<int:skill_id>/tree/children', views.get_children_skills_tree, name='children_skills_tree'),
    path('skills/<int:skill_id>/operations', views.get_operation_skills, name='operation_skills'),
    path('skills/paths/sandbox/', views.get_paths_for_sandbox, name='get-sandbox-paths'),


    path('register/student', views.register_student, name='register_student'),
    path('login/student', views.login_student, name='login_student'),
    path('login/admin', views.login_admin, name='login_admin'),

    path('check-answer/', views.check_answer, name='check-answer'),

    path('chart-data/duration/', views.average_duration, name='average-duration'),   
    path('chart-data/examples/', views.counted_examples, name='counted-examples'),   

]

websocket_urlpatterns = [
    path('ws/speech/', SpeechRecognitionConsumer.as_asgi()),
]

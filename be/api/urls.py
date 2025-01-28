from django.urls import path
from . import views  # Import `views` module

urlpatterns = [
    path('add-example/', views.addExample, name='add-example'),
    path('skills/', views.SkillList.as_view(), name='skill-list'),
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



]

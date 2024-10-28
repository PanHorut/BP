from django.urls import path
from . import views  # Import `views` module

urlpatterns = [
    path('add-example/', views.addExample, name='add-example'),
    path('skills/', views.SkillList.as_view(), name='skill-list'),
    path('get-all-skills/', views.get_all_skills, name='get-all-skills'),
    path('examples-skills/', views.ExampleSkillList.as_view(), name='example-skill-list'),
    path('parent-skills/', views.get_parent_skills, name='get-parent-skills'),
    path('skill/<int:skill_id>/', views.get_skill, name='get-skill'),
    path('examples/', views.get_examples, name='get-examples'),

]

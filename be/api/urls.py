from django.urls import path
from . import views  # Import `views` module

urlpatterns = [
    path('examples/', views.ExampleList.as_view(), name='example-list'),
    path('add-example/', views.addExample, name='add-example'),
    path('skills/', views.SkillList.as_view(), name='skill-list'),
    path('get-all-skills/', views.get_all_skills, name='get-all-skills'),
    path('examples-skills/', views.ExampleSkillList.as_view(), name='example-skill-list'),
]

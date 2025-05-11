"""
================================================================================
 Module: urls.py
 Description:
        Defines the URL routing of the project.

 Author: Dominik Horut (xhorut01)
================================================================================
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def serve_index(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', serve_index),  
    re_path(r'^(?!api/|admin/).*$', serve_index),
]

#if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""
ASGI config for be project.
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from api.consumers import SpeechRecognitionConsumer
from api.consumersSurvey import SurveySpeechTranscriptionConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'be.settings')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/speech/", SpeechRecognitionConsumer.as_asgi()),  
            path("ws/survey/", SurveySpeechTranscriptionConsumer.as_asgi()),
        ])
    ),
})

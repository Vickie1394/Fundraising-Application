# urls.py

from django.urls import path
from .views import dialogflow_chatbot_view

urlpatterns = [
    path('dialogflow-chatbot/', dialogflow_chatbot_view, name='dialogflow_chatbot'),
    # Add other URL patterns as needed
]

from django.urls import path
from . import views 
from django.urls import path
from .views import chatbot_response
 # Import views from the chatbot app

urlpatterns = [
   path('chatbot_response', views.chatbot_response, name='chatbot_response'),  # Add this line
 
    path('open_chat', views.open_chat, name='open_chat'),
]
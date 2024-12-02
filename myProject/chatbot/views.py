from django.http import HttpResponse

from django.shortcuts import render
from django.http import JsonResponse

# Simple keyword-based chatbot
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Example chatbot logic
def chatbot_response(user_input):
    responses = {
        "hello": "Hi there! How can I assist you today?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "bye": "Goodbye! Have a nice day!"
    }
    # Simple response logic
    return responses.get(user_input.lower(), "Sorry, I didn't understand that. Can you try again?")

@csrf_exempt  # Allow POST requests without CSRF token for simplicity
def chat_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get('message', '')
        response_message = chatbot_response(user_message)

        return JsonResponse({"response": response_message})

    return JsonResponse({"error": "Invalid request"}, status=400)
def open_chat(request):

    pass
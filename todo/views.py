from django.http import JsonResponse
from django.shortcuts import render
from .models import TodoItem

def todo_list(request):
    todos = TodoItem.objects.all()
    todos_list = [{"text": todo.text, "completed": todo.completed} for todo in todos]
    return JsonResponse(todos_list, safe=False)

def add_todo(request):
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            TodoItem.objects.create(text=text)
            return JsonResponse({"message": "Todo added successfully!"}, status=201)
        return JsonResponse({"message": "Text is required"}, status=400)

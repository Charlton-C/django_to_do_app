from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import TodoItem

def todo_list(request):
    todos = TodoItem.objects.all()
    return render(request, 'todo_list.html', {'todos': todos})

def add_todo(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            new_todo = TodoItem.objects.create(text=text)
            # Return the new todo item as a JSON response to avoid page reload
            return JsonResponse({
                'id': new_todo.id,
                'text': new_todo.text,
                'completed': new_todo.completed,
            }, status=200)
        else:
            return JsonResponse({'error': 'Todo text is required'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

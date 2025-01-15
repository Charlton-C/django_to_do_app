from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import TodoItem


def todo_list(request):
    todos = TodoItem.objects.all()
    return render(request, 'todo_list.html', {'todos': todos})

def add_todo(request):
    if request.method == 'POST':
        text = request.POST.get('new-todo')
        if text:
            new_todo = TodoItem.objects.create(text=text)
            return JsonResponse({
                'id': new_todo.id,
                'text': new_todo.text,
                'completed': new_todo.completed,
            }, status=200)
        else:
            return JsonResponse({'error': 'Todo text is required'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

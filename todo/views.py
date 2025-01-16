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

def update_todo(request):
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            if id:
                todo = TodoItem.objects.get(id=id)
                if todo:
                    todo.completed = not todo.completed
                    todo.save()
                    return JsonResponse({
                        'success': True,
                        'new_todo_completed': todo.completed
                    }, status=200)
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Todo not found'
                    }, status=400)
            else:
                return JsonResponse({'error': 'Todo id is required'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    except Exception as e:
        return JsonResponse({'error': 'An Internal Server Error Occurred'}, status=500)

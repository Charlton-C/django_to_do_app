from django.http import JsonResponse
from django.shortcuts import render
from .models import TodoItem


def todo_list(request):
    try:
        todos = TodoItem.objects.all()
        return render(request, 'todo_list.html', {'todos': todos})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An Error Occurred'}, status=500)

def add_todo(request):
    try:
        if request.method == 'POST':
            text = request.POST.get('new_todo')
            if text:
                new_todo = TodoItem.objects.create(text=text)
                return JsonResponse({
                    'success': True,
                    'id': new_todo.id,
                    'text': new_todo.text,
                    'completed': new_todo.completed,}, status=200)
            else:
                return JsonResponse({'success': False, 'error': 'Todo text is required'}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An Error Occurred'}, status=500)

def update_todo(request):
    try:
        if request.method == 'POST':
            todo_id = request.POST.get('id')
            if not todo_id:
                return JsonResponse({'success': False, 'error': 'Todo id is required'}, status=400)

            try:
                todo = TodoItem.objects.get(id=todo_id)
            except TodoItem.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Todo not found'}, status=400)

            todo.completed = not todo.completed
            todo.save()

            return JsonResponse({'success': True, 'todo_completed': todo.completed}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An Error Occurred'}, status=500)

def delete_todo(request):
    try:
        if request.method == 'POST':
            todo_id = request.POST.get('id')
            if not todo_id:
                return JsonResponse({'success': False, 'error': 'Todo id is required'}, status=400)

            try:
                todo = TodoItem.objects.get(id=todo_id)
            except TodoItem.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Todo not found'}, status=400)

            todo.delete()
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An Error Occurred'}, status=500)

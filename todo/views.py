from django.shortcuts import render, redirect
from .models import TodoItem

def todo_list(request):
    todos = TodoItem.objects.all()
    return render(request, 'todo_list.html', {'todos': todos})

def add_todo(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            TodoItem.objects.create(text=text)
        return redirect('todo_list')  # Redirect back to the to-do list after adding

    return redirect('todo_list')

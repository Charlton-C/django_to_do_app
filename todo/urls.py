from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),  # Show todo list page
    path('add', views.add_todo, name='add_todo'),  # Add new todo item
]

from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
]

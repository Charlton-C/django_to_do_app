from django.test import TestCase
from todo.models import TodoItem


class TestTodoItemModel(TestCase):

    def test_todo_item_creation(self):
        todo = TodoItem.objects.create(text="Test Todo")
        self.assertEqual(todo.text, "Test Todo")
        self.assertFalse(todo.completed)

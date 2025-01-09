from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from .models import TodoItem

class TodoItemTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.todo_url = reverse('todo_list')
        self.add_todo_url = reverse('add_todo')

        # Create a sample todo item
        self.todo_item = TodoItem.objects.create(text="Test Todo", completed=False)

    def test_todo_list_view(self):
        response = self.client.get(self.todo_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")
        self.assertTemplateUsed(response, 'todo_list.html')

    def test_add_todo_post_valid(self):
        response = self.client.post(self.add_todo_url, {'text': 'New Todo Item'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {
            'id': TodoItem.objects.latest('id').id,
            'text': 'New Todo Item',
            'completed': False,
        })
        self.assertEqual(TodoItem.objects.count(), 2)

    def test_add_todo_post_invalid(self):
        response = self.client.post(self.add_todo_url, {'text': ''})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode(), {'error': 'Todo text is required'})

    def test_add_todo_invalid_method(self):
        response = self.client.get(self.add_todo_url)  # GET request, not allowed
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content.decode(), {'error': 'Invalid request method'})

    def test_todo_list_shows_new_items(self):
        # Adding new item via form submission
        response = self.client.post(self.add_todo_url, {'text': 'Second Todo Item'})
        self.assertEqual(response.status_code, 200)

        # Now check if the second item appears on the todo list page
        response = self.client.get(self.todo_url)
        self.assertContains(response, 'Second Todo Item')
    
    def test_todo_list_no_items(self):
        TodoItem.objects.all().delete()
        response = self.client.get(self.todo_url)
        self.assertContains(response, "No to-dos yet.")

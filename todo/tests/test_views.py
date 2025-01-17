import json

from django.test import TestCase
from django.urls import reverse
from todo.models import TodoItem


class TestTodoListView(TestCase):

    def setUp(self):
        self.todo_item = TodoItem.objects.create(text="Test Todo")

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")

class TestAddTodoView(TestCase):

    def test_add_todo_success(self):
        response = self.client.post(reverse('add_todo'), {'new_todo': 'New Todo'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_add_todo_failure(self):
        response = self.client.post(reverse('add_todo'), {'new_todo': ''})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Todo text is required')

class TestUpdateTodoView(TestCase):

    def setUp(self):
        self.todo_item = TodoItem.objects.create(text="Test Todo")

    def test_update_todo_success(self):
        response = self.client.post(reverse('update_todo'), {'id': self.todo_item.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_update_todo_failure(self):
        response = self.client.post(reverse('update_todo'), {'id': -1})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Todo not found')

    def test_update_todo_no_id(self):
        response = self.client.post(reverse('update_todo'), {})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Todo id is required')

class TestDeleteTodoView(TestCase):

    def setUp(self):
        self.todo_item = TodoItem.objects.create(text="Test Todo")

    def test_delete_todo_success(self):
        response = self.client.post(reverse('delete_todo'), {'id': self.todo_item.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(TodoItem.objects.count(), 0)

    def test_delete_todo_failure(self):
        response = self.client.post(reverse('delete_todo'), {'id': -1})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Todo not found')

    def test_delete_todo_no_id(self):
        response = self.client.post(reverse('delete_todo'), {})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Todo id is required')

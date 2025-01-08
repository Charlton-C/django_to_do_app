from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from .models import TodoItem

class TodoTests(TestCase):

    def setUp(self):
        """Set up initial test data for TodoItems."""
        self.todo_1 = TodoItem.objects.create(text='Finish homework')
        self.todo_2 = TodoItem.objects.create(text='Clean the house')
    
    def test_todo_list_view(self):
        """Test the to-do list view returns the correct data."""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Finish homework')
        self.assertContains(response, 'Clean the house')
        self.assertTemplateUsed(response, 'todo/todo_list.html')

    def test_add_todo_success(self):
        """Test adding a new todo item is successful."""
        response = self.client.post(reverse('add_todo'), {'text': 'Buy groceries'})
        
        # Check if we were redirected back to the list (to verify the data was added)
        self.assertRedirects(response, reverse('todo_list'))
        
        # Check that the new todo item is in the database
        new_todo = TodoItem.objects.get(text='Buy groceries')
        self.assertIsNotNone(new_todo)
        self.assertEqual(new_todo.text, 'Buy groceries')
        self.assertFalse(new_todo.completed)  # By default, new todos are not completed

    def test_add_todo_failure_empty_text(self):
        """Test that adding a todo with empty text returns an error."""
        response = self.client.post(reverse('add_todo'), {'text': ''})
        
        # Check that the response status code is 302 (redirect to the todo list page)
        self.assertRedirects(response, reverse('todo_list'))
        
        # Check that the number of TodoItems hasn't changed
        self.assertEqual(TodoItem.objects.count(), 2)
        
    def test_todo_item_checkbox_is_disabled(self):
        """Test that the checkbox is disabled in the UI."""
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, '<input type="checkbox" disabled>', count=2)
    
    def test_add_duplicate_todo(self):
        """Test adding a duplicate todo."""
        # Trying to add a duplicate task
        response = self.client.post(reverse('add_todo'), {'text': 'Finish homework'})
        
        # Check that we still only have one instance of this task
        self.assertEqual(TodoItem.objects.filter(text='Finish homework').count(), 1)
    
    def test_api_add_todo_invalid_method(self):
        """Test that an invalid HTTP method results in a 405 error."""
        response = self.client.get(reverse('add_todo'))  # GET instead of POST
        self.assertEqual(response.status_code, 405)  # Method not allowed

# Tests for the user API

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:register')

def create_user(**params):
	# Create and return a new user
	return get_user_model().objects.create_user(**params)

class PublicUserTests(TestCase):
	# Test the public features of the API
	def setUp(self):
		self.client = APIClient()

	def test_create_user_success(self):
		# Test creating a user successful
		data = {
		'name':'Test Name',
		'email':'test@example.com',
		'username':'TestUsername',
		'secret_keyword':'testsecretkw',
		'password':'testpass123'
		}
		result = self.client.post(CREATE_USER_URL, data)
		self.assertEqual(result.status_code, status.HTTP_201_CREATED)
		user = get_user_model().objects.get(email=data['email'])
		self.assertTrue(user.check_password(data['password']))
		# Check that we do not return the password to the user
		self.assertNotIn('password', result.data)

	def test_user_with_same_email_exist(self):
		# Test error returned if user with this email already exists
		data = {
		'name':'Test Name',
		'email':'test@example.com',
		'username':'TestUsername',
		'secret_keyword':'testsecretkw',
		'password':'testpass123'
		}
		create_user(**data)
		result = self.client.post(CREATE_USER_URL, data)
		self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

	def test_password_too_short(self):
		# Test if user is using too short password
		data = {
		'name':'Test Name',
		'email':'test@example.com',
		'username':'TestUsername',
		'secret_keyword':'testsecretkw',
		'password':'pw'
		}
		result = self.client.post(CREATE_USER_URL, data)
		self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
		# Check that the user is not created due to too short password
		user_exists = get_user_model().objects.filter(email=data['email']).exists()
		self.assertFalse(user_exists)
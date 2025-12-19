# Tests for recipe APIs

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core import models
from recipe import serializers


RECIPES_URL = reverse('recipes-list')

def create_recipe(author,params):
	# Create and return sample recipe
	defaults = {
	'title':'Sample Recipe',
	'time_minutes':20,
	'price':Decimal('5.50'),
	'description':'Sample description',
	'link':'http://example.com/recipe.pdf:'
	}
	defaults.update(params)
	recipe = models.Recipe.objects.create(author=author,**defaults)
	return recipe


class PublicRecipeAPITests(TestCase):
	# Test unauthenticated API requests
	def setUp(self):
		self.client = APIClient()
	def test_auth_required(self):
		# Test authentication is required to call API
		res = self.client.get(RECIPES_URL)
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
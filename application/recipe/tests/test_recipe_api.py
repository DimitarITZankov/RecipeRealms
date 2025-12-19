# Tests for recipe APIs

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core import models
from recipe import serializers


RECIPES_URL = reverse('recipe:recipes-list')

def detail_url(recipe_id):
	# Create and return a recipe detail URL
	return reverse('recipe:recipes-detail', args=[recipe_id])


def create_recipe(author,**params):
	# Create and return sample recipe
	defaults = {
	'title':'Sample Recipe',
	'time_minutes':20,
	'description':'Sample description',
	}
	defaults.update(params)
	recipe = models.Recipes.objects.create(author=author,**defaults)
	return recipe


class PublicRecipeAPITests(TestCase):
	# Test unauthenticated API requests
	def setUp(self):
		self.client = APIClient()
	def test_auth_required(self):
		# Test authentication is required to call API
		result = self.client.get(RECIPES_URL)
		self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITests(TestCase):
	# Test authenticated API requests
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user('user@example.com','examplepass123')
		self.client.force_authenticate(self.user)

	def test_retrieve_recipes(self):
		# Test retrieving a list of recipes
		create_recipe(author=self.user)
		create_recipe(author=self.user)
		result = self.client.get(RECIPES_URL)
		recipes = models.Recipes.objects.all().order_by('-id')
		serializer = serializers.RecipeSerializer(recipes,many=True)
		self.assertEqual(result.status_code, status.HTTP_200_OK)
		self.assertEqual(result.data,serializer.data)

	def test_get_recipe_detail(self):
		# Test get recipe detail
		recipe = create_recipe(author=self.user)
		url = detail_url(recipe.id)
		result = self.client.get(url)
		serializer = serializers.RecipeDetailSerializer(recipe)
		self.assertEqual(result.data, serializer.data)

	def test_create_recipe_with_new_tags(self):
		# Test creating a recipe with new tags
		payload = {
			'title':'Thai Prawn Curry',
			'time_minutes':30,
			'tags':[{'name':'Thai'},{'name':'Dinner'}]
		}
		result = self.client.post(RECIPES_URL,payload, format='json')
		self.assertEqual(result.status_code, status.HTTP_201_CREATED)
		recipes = models.Recipes.objects.filter(author=self.user)
		self.assertEqual(recipes.count(), 1)
		recipe = recipes[0]
		self.assertEqual(recipe.tags.count(),2)
		for tag in payload['tags']:
			exists = recipe.tags.filter(name=tag['name'],author=self.user,).exists()
			self.assertTrue(exists)

	def test_create_recipe_with_existing_tags(self):
		# Test creating a recipe with existing tag
		tag_indian = models.Tag.objects.create(author=self.user,name='Indian')
		payload = {
			'title':'Pongal',
			'time_minutes':60,
			'tags':[{'name':'Indian'},{'name':'Breakfast'}],
		}
		result = self.client.post(RECIPES_URL, payload, format='json')
		self.assertEqual(result.status_code, status.HTTP_201_CREATED)
		recipes = models.Recipes.objects.filter(author=self.user)
		self.assertEqual(recipes.count(), 1)
		recipe = recipes[0]
		self.assertEqual(recipe.tags.count(), 2)
		self.assertIn(tag_indian, recipe.tags.all())
		for tag in payload['tags']:
			exists = recipe.tags.filter(name=tag['name'],author=self.user,).exists()
			self.assertTrue(exists)
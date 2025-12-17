# Models for the database
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager,)
from django.conf import settings
import uuid
import os

def recipe_image_file_path(instance,filename):
	# Generate filepath for the new recipe image
	ext = os.path.splitext(filename)[1]
	filename = f'{uuid.uuid4()}{ext}'
	return os.path.join('uploads','recipe',filename)

def profile_image_file_path(instance,filename):
	# Generate filepath for the new recipe image
	ext = os.path.splitext(filename)[1]
	filename = f'{uuid.uuid4()}{ext}'
	return os.path.join('uploads','profile',filename)

class CustomUserManager(BaseUserManager):
	# Create Custom base user manager
	# Create basic user
	def create_user(self,email,password=None,**extra_fields):
		if not email:
			raise ValueError("Every user must provide an email")
		user = self.model(email=self.normalize_email(email),**extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	# Create superuser using the django CLI
	def create_superuser(self,email,password,**extra_fields):
		user = self.create_user(email,password,**extra_fields)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser,PermissionsMixin):
	# Create custom user model
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=255,unique=True)
	username = models.CharField(max_length=30,unique=True)
	secret_keyword = models.CharField(max_length=255,null=False,blank=False)
	profile_image = models.ImageField(null=True,blank=True,upload_to=profile_image_file_path)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	# Assign our model to the custom user manager
	objects = CustomUserManager()

	# Login and required fields
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name','username','secret_keyword']

	# Helper funtions
	def get_full_name(self):
		return self.name
	def get_short_name(self):
		return self.name
	def __str__(self):
		return self.username

class Recipes(models.Model):
	# Create table for the recipes
	author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	description = models.TextField(max_length=1000)
	time_minutes = models.IntegerField()
	difficulty = models.CharField(max_length=15)
	tags = models.ManyToManyField('Tag')
	products = models.ManyToManyField('Products')
	image = models.ImageField(null=True,upload_to=recipe_image_file_path)

	def __str__(self):
		return self.title

class Tag(models.Model):
	# Adding table for tags
	name = models.CharField(max_length=255)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	class Meta:
		unique_together = ('name','author')

	def __str__(self):
		return self.name


class Products(models.Model):
	# Create a products table for storing all the products
	name = models.CharField(max_length=255)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	class Meta:
		unique_together = ('name','author')
	def __str__(self):
		return self.name


class Comments(models.Model):
	# Create a comments table for storing all the comments for each recipe
	content = models.TextField(max_length=500)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	recipe = models.ForeignKey('Recipes',related_name='comments',on_delete=models.CASCADE)

	def __str__(self):
		return self.author.username

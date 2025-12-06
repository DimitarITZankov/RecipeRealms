# Models for the database
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager,)

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
	def create_superuser(self,email,password):
		user = self.create_user(email,password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser,PermissionsMixin):
	# Create custom user model
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=255,unique=True)
	username = models.CharField(max_length=30,unique=True)
	secret_keyword = models.CharField(max_length=255,null=False)
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
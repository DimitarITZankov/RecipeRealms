from rest_framework import serializers
from core import models
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
	# Create Register serializer
	password = serializers.CharField(write_only=True)
	class Meta:
		model = get_user_model()
		fields = ['name','email','username','secret_keyword','password']
		extra_kwargs = {'password':{'write_only':True,'style':{'input_type':'password'}},'secret_keyword':{'write_only':True,'style':{'input_type':'password'}}}
	def create(self,validated_data):
		user = get_user_model().objects.create_user(**validated_data)
		return user
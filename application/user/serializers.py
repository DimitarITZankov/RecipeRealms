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

class ChangePasswordSerializer(serializers.Serializer):
	# Change password
	old_password = serializers.CharField()
	new_password_first = serializers.CharField()
	new_password_second = serializers.CharField()

	def validate(self,attrs):
		user = self.context['request'].user

		# Check if old password match
		if not user.check_password(attrs['old_password']):
			raise serializers.ValidationError('Old password is incorrect')

		# Check if the new password match
		if attrs['new_password_first'] != attrs['new_password_second']:
			raise serializers.ValidationError("Passwords do not match")

		return attrs
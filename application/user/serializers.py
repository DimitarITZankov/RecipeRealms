from rest_framework import serializers
from core import models
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
	# Create Register serializer
	password = serializers.CharField(write_only=True,style={'input_type': 'password'})
	class Meta:
		model = get_user_model()
		fields = ['name','email','username','secret_keyword','password']
		extra_kwargs = {'password':{'write_only':True,'style':{'input_type':'password'}},'secret_keyword':{'write_only':True,'style':{'input_type':'password'}}}
	def create(self,validated_data):
		user = get_user_model().objects.create_user(**validated_data)
		return user

	def validate_password(self, value):
		# Validate the password using Django's built-in validators
		validate_password(value)
		return value

class ChangePasswordSerializer(serializers.Serializer):
	# Change password
	old_password = serializers.CharField(write_only=True)
	new_password_first = serializers.CharField(write_only=True)
	new_password_second = serializers.CharField(write_only=True)

	def validate(self,attrs):
		user = self.context['request'].user

		# Check if old password match
		if not user.check_password(attrs['old_password']):
			raise serializers.ValidationError('Old password is incorrect')

		# Check if the new password match
		if attrs['new_password_first'] != attrs['new_password_second']:
			raise serializers.ValidationError("Passwords do not match")

		return attrs

class ResetPasswordSerializer(serializers.Serializer):
	# Reset password using the 'secret_keyword' field
	secret_keyword = serializers.CharField()
	new_password_first = serializers.CharField(write_only=True)
	new_password_second = serializers.CharField(write_only=True)

	def validate_secret_keyword(self,value):
		# Check if the keyword match the one assigned to the user
		user = self.context['request'].user
		if value != user.secret_keyword:
			raise serializers.ValidationError("Secret keyword is wrong")
		return value

	def validate(self,attrs):
		# Check if the new password matches both of the fields
		user = self.context['request'].user
		if attrs['new_password_first'] != attrs['new_password_second']:
			raise serializers.ValidationError("Passwords do not match")

		# Validate the password using Django's password validator
		validate_password(attrs['new_password_first'])
		return attrs

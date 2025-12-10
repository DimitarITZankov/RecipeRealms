from rest_framework import serializers
from core import models

class RecipeSerializer(serializers.ModelSerializer):
	# Create serializer for creating a recipes
	class Meta:
		model = models.Recipes
		fields = ['id','author','title','time_minutes','difficulty',]
		read_only_fields = ('id','author','difficulty')

	def create(self, validated_data):
		time = validated_data['time_minutes']
		# Assign difficulty based on the time
		if time <= 30:
			validated_data['difficulty'] = 'Easy'
		elif time <=60:
			validated_data['difficulty'] = 'Medium'
		else:
			validated_data['difficulty'] = 'Hard'
		recipe = models.Recipes.objects.create(**validated_data)
		return recipe

	def update(self,instance,validated_data):
		# Update the time if changed
		time = validated_data.get('time_minutes', instance.time_minutes)
		if time <= 30:
			instance.difficulty = 'Easy'
		elif time <= 60:
			instance.difficulty = 'Medium'
		else:
			instance.difficulty = 'Hard'
		for attr,value in validated_data.items():
			setattr(instance,attr,value)
		instance.save()
		return instance

	def get_author_name(self, obj):
		# Get the author's name instead of ID by default
		return obj.author.name

class RecipeDetailSerializer(RecipeSerializer):
	# Create a detailed view serializer for the recipes
	class Meta(RecipeSerializer.Meta):
		fields = RecipeSerializer.Meta.fields + ['description','products']
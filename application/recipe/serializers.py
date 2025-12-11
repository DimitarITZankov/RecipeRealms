from rest_framework import serializers
from core import models

class TagSerializer(serializers.ModelSerializer):
	# Serializers for tags
	class Meta:
		model = models.Tag
		fields = ['id','name']
		read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
	# Create serializer for creating a recipes
	tags = TagSerializer(many=True, required=False)
	class Meta:
		model = models.Recipes
		fields = ['id','author','title','time_minutes','difficulty','tags']
		read_only_fields = ('id','author','difficulty')

	def _get_or_create_tags(self, tags, recipe):
		# Handle creating or getting tag if needed (tags are global, not attached per user)
		for tag in tags:
			tag_obj, created = models.Tag.objects.get_or_create(name=tag['name'])
			recipe.tags.add(tag_obj)

	def create(self, validated_data):
		time = validated_data['time_minutes']
		# Assign difficulty based on the time
		if time <= 30:
			validated_data['difficulty'] = 'Easy'
		elif time <=60:
			validated_data['difficulty'] = 'Medium'
		else:
			validated_data['difficulty'] = 'Hard'
		tags = validated_data.pop('tags',[])
		recipe = models.Recipes.objects.create(**validated_data)
		self._get_or_create_tags(tags,recipe)
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
		tags = validated_data.pop('tags',None)
		if tags is not None:
			instance.tags.clear()
			self._get_or_create_tags(tags,instance)
		for attr,value in validated_data.items():
			setattr(instance,attr,value)
		instance.save()
		return instance

class RecipeDetailSerializer(RecipeSerializer):
	# Create a detailed view serializer for the recipes
	class Meta(RecipeSerializer.Meta):
		fields = RecipeSerializer.Meta.fields + ['description','products']
from django.shortcuts import render
from recipe import serializers, permissions
from core import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class RecipeViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.RecipeDetailSerializer
	permission_classes = [IsAuthenticated,permissions.IsOwnerOrReadOnly]
	queryset = models.Recipes.objects.all()

	def get_queryset(self):
	# Return recipes for the authenticated user
		return self.queryset.all().order_by('-id')

	def perform_create(self,serializer):
	# Assign the authenticated user to author of the new recipe
		return serializer.save(author=self.request.user)

	def get_serializer_class(self):
	# Return the right serializer based on the request
		if self.action == 'list':
			return serializers.RecipeSerializer
		return self.serializer_class


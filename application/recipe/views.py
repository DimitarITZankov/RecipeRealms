from django.shortcuts import render
from recipe import serializers, permissions
from core import models
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

class RecipeViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.RecipeDetailSerializer
	permission_classes = [IsAuthenticated,permissions.IsOwnerOrReadOnly]
	queryset = models.Recipes.objects.all()
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['tags','title','products__name']


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
		elif self.action == 'upload_image':
			return serializers.RecipeImageSerializer
		return self.serializer_class

	@action(methods=['POST','PATCH','PUT','DELETE'],detail=True,url_path='upload-image')
	def upload_image(self,request,pk=None):
		# Upload an image to recipe
		recipe = self.get_object()
		if request.method == 'DELETE':
			# Remove the image file and save it
			recipe.image.delete(save=True)
			serializer= self.get_serializer(recipe)
			return Response(serializer.data, status=status.HTTP_200_OK)

		serializer = self.get_serializer(recipe,data=request.data,partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductsViewSet(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
	# Manage products in the database
	serializer_class = serializers.ProductsSerializer
	authentication_classes = [JWTAuthentication,]
	permission_classes = [IsAuthenticated,]
	queryset = models.Products.objects.all()
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['name']

	def get_queryset(self):
		# Show only products by the authenticated user
		return self.queryset.filter(author=self.request.user).order_by('-name')
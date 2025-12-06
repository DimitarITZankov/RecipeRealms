from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import viewsets, generics, status
from user.permissions import IsNotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from user import serializers
from core import models

# Register API
class RegisterUserViewSet(generics.CreateAPIView):
	serializer_class = serializers.RegisterSerializer
	permission_classes = [IsNotAuthenticated,]

	def create(self,request,*args,**kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({"message":"User registered successfully"}, status=status.HTTP_201_CREATED)

# Create User Profile API
class UserProfileViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.RegisterSerializer
	authentication_classes = [JWTAuthentication,]
	permission_classes = [IsAuthenticated,]
	queryset = models.User.objects.all()

	# Allow only these HTTP methods
	http_method_names = ['get', 'put', 'patch']

	# Return only the logged-in user
	def get_queryset(self):
		return self.queryset.filter(pk=self.request.user.pk) # Primary key

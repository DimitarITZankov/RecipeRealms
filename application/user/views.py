from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import viewsets, generics, status
from user.permissions import IsNotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from user import serializers
from core import models
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

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

# Create View for change password
class ChangePasswordView(generics.UpdateAPIView):
	serializer_class = serializers.ChangePasswordSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def get_object(self):
		return self.request.user

	def perform_update(self,serializer):
		user = self.request.user
		new_password = serializer.validated_data['new_password_first']
		user.set_password(new_password)
		user.save()

# Create View for reset password
class ResetPasswordView(generics.UpdateAPIView):
	serializer_class = serializers.ResetPasswordSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def get_object(self):
		return self.request.user

	def perform_update(self,serializer):
		user = self.request.user
		new_password = serializer.validated_data['new_password_first']
		user.set_password(new_password)
		user.save()

# Create View for uploading profile image
class UploadProfileImageView(generics.UpdateAPIView):
    serializer_class = serializers.ProfileImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Optional: allow POST too
        return self.patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.profile_image.delete(save=True)  # Deletes the file and updates the model
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
	path('jwt/create', TokenObtainPairView.as_view(), name='jwt-create'),
	path('jwt/refresh', TokenRefreshView.as_view(), name='jwt-refresh'),
]
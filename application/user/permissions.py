# Custom permissions for the API
from rest_framework import permissions

class IsNotAuthenticated(permissions.BasePermission):
	# Allow access only to unauthenticated users
	def has_permission(self,request,view):
		return not request.user or not request.user.is_authenticated

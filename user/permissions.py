from rest_framework import permissions

class IsOwner(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if obj.user == request.user:
      return True
    return False

class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    elif obj.user == request.user:
      return True
    return False

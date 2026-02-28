from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
  def has_permission(self, request, view):
    return request.user.role == "superadmin"
  
class IsAdmin(BasePermission):
  def has_permission(self, request, view):
    return request.user.role == "admin"
  
class IsUser(BasePermission):
  def has_permission(self, request, view):
    return request.user.role == "user"

class IsAdminOrSuperAdmin(BasePermission):
  def has_permission(self, request, view):
    return request.user.role in ["admin","superadmin"]
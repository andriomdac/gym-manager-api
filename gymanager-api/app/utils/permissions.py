from rest_framework.permissions import BasePermission
from icecream import ic


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role.name == "manager"


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role.name == "staff"
    
    
class AllowRoles(BasePermission):
    
    def __init__(self, roles_allowed: list=[]):
        self.allowed_roles = roles_allowed
        
    def has_permission(self, request, view):
        if request.user.profile.role.name in self.allowed_roles:
            return True
        if request.user.profile.role.name == "admin":
            return True
        return False
        
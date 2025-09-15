from rest_framework.permissions import BasePermission
from icecream import ic


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role.name == "manager"
    
class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role.name == "staff"
    

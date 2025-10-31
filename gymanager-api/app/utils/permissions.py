from rest_framework.permissions import BasePermission

    
class  AllowRoles(BasePermission):
    
    def __init__(self, roles_allowed: list=[]):
        self.allowed_roles = roles_allowed
        
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.profile.role.name in self.allowed_roles:
            return True
        if request.user.profile.role.name == "admin":
            return True
        return False
        

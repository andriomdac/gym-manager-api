from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from gyms.models import Gym
from roles.models import Role


class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT, related_name='profile', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='role', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.uuid}"

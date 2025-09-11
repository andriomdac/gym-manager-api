from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from gyms.models import Gym


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT, related_name='profile', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.uuid}"
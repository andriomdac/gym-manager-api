from django.db import models
from uuid import uuid4


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

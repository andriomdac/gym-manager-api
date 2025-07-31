from uuid import uuid4
from django.db import models


class Gym(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    reference = models.CharField(max_length=255)

    def __str__(self):
        return self.name

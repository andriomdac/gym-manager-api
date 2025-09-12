from django.db import models
from uuid import uuid4

class PaymentMethod(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

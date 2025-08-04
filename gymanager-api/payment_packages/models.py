from django.db import models
from uuid import uuid4

class PaymentPackage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
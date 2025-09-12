from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator


class PaymentPackage(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=10)
    duration_days = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(372)])

    def __str__(self):
        return self.name

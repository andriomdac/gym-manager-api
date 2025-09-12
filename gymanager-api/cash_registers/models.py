from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator
from gyms.models import Gym


class CashRegister(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    gym = models.ForeignKey(to=Gym, on_delete=models.PROTECT, related_name="cash_registers", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    register_date = models.DateField(unique=True)
    is_opened = models.BooleanField(default=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0.00)]
    )

    def __str__(self):
        return f"{self.register_date}"

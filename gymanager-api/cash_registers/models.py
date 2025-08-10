from django.db import models
from uuid import uuid4


class CashRegister(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    register_date = models.DateField(unique=True)
    is_opened = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.register_date}"
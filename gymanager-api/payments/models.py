from uuid import uuid4
from django.db import models
from students.models import Student
from payment_packages.models import PaymentPackage
from cash_registers.models import CashRegister
from django.core.validators import MinValueValidator
from payment_methods.models import PaymentMethod


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_date = models.DateField(blank=True, null=True)
    next_payment_date = models.DateField(blank=True, null=True)
    student = models.ForeignKey(
        to=Student,
        on_delete=models.PROTECT,
        related_name='payments'
    )
    payment_package = models.ForeignKey(
        to=PaymentPackage,
        on_delete=models.PROTECT,
        related_name='payments'
    )
    cash_register = models.ForeignKey(
        to=CashRegister,
        on_delete=models.PROTECT,
        related_name="payments"
    )
    observations = models.CharField(max_length=255, blank=True, null=True)
    receiver = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.payment_date}"


class PaymentValue(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    payment = models.ForeignKey(
        to=Payment,
        on_delete=models.CASCADE,
        related_name='payment_values'
    )
    payment_method = models.ForeignKey(
        to=PaymentMethod,
        on_delete=models.PROTECT,
        related_name='payment_values'
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.payment} - {self.value}"

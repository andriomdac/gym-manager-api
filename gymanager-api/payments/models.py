from django.db import models
from django.core.validators import MinValueValidator
from students.models import Student
from payment_packages.models import PaymentPackage
from payment_methods.models import PaymentMethod
from uuid import uuid4
from cash_registers.models import CashRegister


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
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
    observations = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.payment_date}"


class PaymentValue(models.Model):
    payment = models.ForeignKey(
        to=Payment,
        on_delete=models.PROTECT,
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
        validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.payment} - {self.value}"

from rest_framework.generics import get_object_or_404
from .models import CashRegister


def update_cash_register_amount(register_id: str) -> None:
    register = get_object_or_404(CashRegister, id=register_id)
    register.amount = 0
    for payment in register.payments.all():
        for value in payment.payment_values.all():
            register.amount += value.value
    register.save()
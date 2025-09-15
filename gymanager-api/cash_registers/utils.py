from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from datetime import datetime
from .models import CashRegister

def build_cash_resgister_serializer(
    serializer_instance: Serializer,
    gym_id: str
    ) -> Response:
    data = serializer_instance.initial_data
    data["gym"] = gym_id
    if not "register_date" in data:
        data["register_date"] = datetime.today().date()
    return serializer_instance


def update_cash_register_amount(register_id: str) -> None:
    register = get_object_or_404(CashRegister, id=register_id)
    register.amount = 0
    for payment in register.payments.all():
        for value in payment.payment_values.all():
            register.amount += value.value
    register.save()
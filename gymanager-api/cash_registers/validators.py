from rest_framework.serializers import Serializer
from django.utils import timezone
from .models import CashRegister


def validate_cash_resgister_serializer(serializer) -> Serializer:
    data = serializer.initial_data
    if not "register_date" in data:
        data["register_date"] = timezone.localdate()
    new_serializer = CashRegisterSerializer(data=data)
    return new_serializer


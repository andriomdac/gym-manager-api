from rest_framework.serializers import Serializer
from .models import PaymentMethod
from app.utils.exceptions import CustomValidatorException


def validate_payment_method(serializer: Serializer) -> Serializer:
    data = serializer.validated_data
    if PaymentMethod.objects.filter(name=data["name"]).exists():
        raise CustomValidatorException("payment method with same name already exists.")
    return serializer
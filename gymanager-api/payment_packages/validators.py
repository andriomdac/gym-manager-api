from rest_framework.serializers import Serializer
from .models import PaymentPackage
from app.utils.exceptions import CustomValidatorException


def validate_payment_package(serializer: Serializer) -> Serializer:
    data = serializer.validated_data
    if PaymentPackage.objects.filter(name=data["name"]).exists():
        raise CustomValidatorException("payment package with same name already exists.")
    return serializer
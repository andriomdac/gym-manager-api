from rest_framework.serializers import Serializer
from app.utils.exceptions import CustomValidatorException
from .models import Gym


def validate_gym_serializer(serializer_instance) -> Serializer:
    data = serializer_instance.validated_data
    if Gym.objects.filter(
        name=data["name"],
        reference=data["reference"]
    ).exists():
        raise CustomValidatorException(
            "Academia com este nome e referência já existe."
            )
    return serializer_instance

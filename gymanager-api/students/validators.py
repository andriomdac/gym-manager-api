from rest_framework.serializers import Serializer
from app.utils.exceptions import CustomValidatorException
from .models import Student


def validate_student_serializer(
    serializer_instance: Serializer,
    gym_id
    ) -> Serializer:
    data = serializer_instance.initial_data

    data["gym"] = gym_id

    if Student.objects.filter(
        name=data.get("name", ""),
        reference=data.get("reference", "")).exists():
        raise CustomValidatorException("Aluno com mesmo nome e referência já existe.")
    return serializer_instance

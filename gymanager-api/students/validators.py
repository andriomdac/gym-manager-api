from rest_framework.serializers import Serializer
from app.utils.exceptions import CustomValidatorException
from .models import Student


def validate_student_serializer(
    serializer_instance: Serializer,
    gym_id
    ) -> Serializer:
    data = serializer_instance.initial_data

    data["gym"] = gym_id

    if "name" in data and "reference" in data:
        if Student.objects.filter(
            name=data["name"],
            reference=data["reference"]).exists():
            raise CustomValidatorException("student with this name and reference already exists.")
    return serializer_instance

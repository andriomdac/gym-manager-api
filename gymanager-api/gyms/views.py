from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .models import Gym
from .serializers import GymSerializer
from app.utils.exceptions import CustomValidatorException


from icecream import ic


@api_view(["GET", "POST"])
def gym_list_create_view(request: Request) -> Response:
    if request.method == "GET":
        gyms = Gym.objects.all().order_by("name")
        serializer = GymSerializer(instance=gyms, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        try:
            data = request.data
            serializer = GymSerializer(data=request.data)
            if serializer.is_valid():

                serializer_data = serializer.validated_data
                if Gym.objects.filter(
                    name=serializer_data["name"],
                    reference=serializer_data["reference"]
                    ).exists():
                    raise CustomValidatorException("Gym with this name and reference already exists.")

                return Response(data=serializer.data)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"})




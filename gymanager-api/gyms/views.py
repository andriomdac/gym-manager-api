from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import Gym
from .serializers import GymSerializer
from app.utils.exceptions import CustomValidatorException
from .validators import validate_gym_serializer
from app.utils.paginator import paginate_serializer
from rest_framework.pagination import PageNumberPagination
from app.utils.permissions import AllowRoles


class GymListCreateAPIView(APIView):
    
    def get_permissions(self):
        return [AllowRoles()]
    
    def get(self, request: Request) -> Response:
        gyms = Gym.objects.all().order_by("name")
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=gyms,
            request=request,
            serializer=GymSerializer,
            paginator=paginator
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        try:
            data = request.data
            serializer = GymSerializer(data=data)
            if serializer.is_valid():
                serializer = validate_gym_serializer(serializer)
                serializer.save()
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                    )

        except CustomValidatorException as e:
            return Response({"detail": f"{e}"})


class GymRetrieveUpdateDestroyAPIView(APIView):

    def get_permissions(self):
        return [AllowRoles()]

    def get(self, request: Request, gym_id: int) -> Response:
        gym = get_object_or_404(Gym, id=gym_id)
        serializer = GymSerializer(gym)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, gym_id: int) -> Response:
        try:
            gym = get_object_or_404(Gym, id=gym_id)
            data = request.data
            serializer = GymSerializer(instance=gym, data=data)

            if serializer.is_valid():
                serializer = validate_gym_serializer(serializer)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_200_OK)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"})

    def delete(self, request: Request, gym_id: int) -> Response:
        gym = get_object_or_404(Gym, id=gym_id)
        gym.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import Student, StudentStatus
from gyms.models import Gym
from .serializers import StudentSerializer, StudentStatusSerializer
from app.utils.exceptions import CustomValidatorException
from .validators import validate_student_serializer
from app.utils.paginator import paginate_serializer
from rest_framework.pagination import PageNumberPagination
from app.utils.permissions import AllowRoles


class StudentListCreateAPIView(APIView):

    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def get(
        self,
        request: Request,
        gym_id: str
        ) -> Response:
        gym = get_object_or_404(Gym, id=gym_id)
        students = Student.objects.filter(gym=gym).order_by("name")
        
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=students,
            request=request,
            serializer=StudentSerializer,
            paginator=paginator
        )
        
        return paginator.get_paginated_response(serializer.data)

    def post(
        self,
        request: Request,
        gym_id: str
        ) -> Response:
        try:
            data = request.data
            serializer = StudentSerializer(data=data)
            serializer = validate_student_serializer(
                serializer_instance=serializer,
                gym_id=gym_id
                )
            if serializer.is_valid():
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
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class StudentRetrieveUpdateDestroyAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowRoles(["staff", "manager"])]
        return [AllowRoles(["manager"])]

    def get(
        self,
        request: Request,
        gym_id: str,
        student_id: str
        ) -> Response:
        student = get_object_or_404(Student, id=student_id)
        serializer = StudentSerializer(student)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(
        self,
        request: Request,
        gym_id: str,
        student_id: str
        ) -> Response:
        try:
            student = get_object_or_404(Student, id=student_id)
            data = request.data
            serializer = StudentSerializer(instance=student, data=data)

            if serializer.is_valid():
                serializer = validate_student_serializer(serializer)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_200_OK)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"})

    def delete(
        self,
        request: Request,
        gym_id: str,
        student_id: str,
        ) -> Response:
        student = get_object_or_404(Student, id=student_id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentStatusListUpdateAPIView(APIView):
    
    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def get(
        self,
        request: Request,
        gym_id: str
        ) -> Response:

        students_status = StudentStatus.objects.filter(student__gym=gym_id)
        serializer = StudentStatusSerializer(instance=students_status, many=True)
        return Response(serializer.data)


    def post(
        self,
        request: Request,
        gym_id: str
        ) -> Response:
        
        today = timezone.localdate()
        for student in Student.objects.filter(gym=gym_id):
            last_payment = student.payments.order_by("next_payment_date").last()
            if last_payment:
                status = StudentStatus.objects.get(student=student)
                if today > last_payment.next_payment_date:
                    status.is_overdue = False
                    status.save()
        return Response()


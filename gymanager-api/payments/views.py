from typing import Type
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from students.models import Student
from .serializers import PaymentSerializer
from django.utils import timezone
from icecream import ic
from datetime import datetime, timedelta


def get_next_payment_date(payment_date: datetime, payment_package: str) -> datetime:
    return payment_date + timedelta(days=31)


def validate_payment_serializer(serializer: Serializer, student_id: str) -> Serializer:
    data = serializer.initial_data
    if not "payment_date" in data:
        data["payment_date"] = timezone.localdate()
    data["next_payment_date"] = get_next_payment_date(
        payment_date=data["payment_date"],
        payment_package=data["payment_package"]
        )
    data["student"] = student_id
    

    new_serializer = PaymentSerializer(data=data)
    return new_serializer


class PaymentsListCreateAPIView(APIView):

    def get(self, request: Request, student_id: str) -> Response:
        student = get_object_or_404(Student, id=student_id)
        student_payments = student.payments.all()
        serializer = PaymentSerializer(instance=student_payments, many=True)
        return Response(serializer.data)


    def post(self, request: Request, student_id: str) -> Response:
        student = get_object_or_404(Student, id=student_id)
        data = request.data
        serializer = PaymentSerializer(data=data)

        serializer = validate_payment_serializer(
            serializer=serializer,
            student_id=student_id
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


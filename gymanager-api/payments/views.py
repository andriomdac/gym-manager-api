from typing import Type
from app.utils.exceptions import CustomValidatorException
from rest_framework.request import Request
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from students.models import Student
from .serializers import PaymentSerializer, PaymentListSerializer
from django.utils import timezone
from icecream import ic
from datetime import datetime, timedelta
from cash_registers.models import CashRegister
from datetime import datetime


def get_next_payment_date(payment_date: datetime, payment_package: str) -> datetime:
    return payment_date + timedelta(days=31)


def validate_payment_serializer(serializer: Serializer, student_id: str) -> Serializer:
    data = serializer.initial_data
    cash_register = get_object_or_404(CashRegister, id=data["cash_register"])

    if "payment_date" in data:
        payment_date = datetime.strptime(data["payment_date"], "%Y-%m-%d").date()
    else:
        payment_date = timezone.localdate()

    if cash_register.payments.filter(payment_date=payment_date).exists():
        raise CustomValidatorException("there is already a payment of this student in this cash register")

    data["next_payment_date"] = get_next_payment_date(
        payment_date=payment_date,
        payment_package=data["payment_package"]
        )
    data["student"] = student_id

    if not cash_register.is_opened:
        raise CustomValidatorException("Cannot add new payment to a closed cash register.")
    
    if not payment_date == cash_register.register_date:
        raise CustomValidatorException("payment date must be the same as the cash register date")

    new_serializer = PaymentSerializer(data=data)
    return new_serializer


class PaymentsListCreateAPIView(APIView):

    def get(self, request: Request, student_id: str) -> Response:
        student = get_object_or_404(Student, id=student_id)
        student_payments = student.payments.all()
        serializer = PaymentListSerializer(instance=student_payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request, student_id: str) -> Response:
        try:
            student = get_object_or_404(Student, id=student_id)
            data = request.data
            serializer = PaymentSerializer(data=data)

            serializer = validate_payment_serializer(
                serializer=serializer,
                student_id=student_id
                )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

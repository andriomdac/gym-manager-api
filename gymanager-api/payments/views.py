from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from app.utils.exceptions import CustomValidatorException
from students.models import Student
from .models import Payment, PaymentValue
from payment_methods.models import PaymentMethod
from cash_registers.models import CashRegister
from .serializers import PaymentSerializer, PaymentValueSerializer
from .validators import validate_payment_deletion, validate_payment_value_serializer, validate_payment_serializer
from .serializer_builders import build_payment_serializer






from icecream import ic

def update_cash_register_amount(register_id: str) -> None:
    register = get_object_or_404(CashRegister, id=register_id)
    for payment in register.payments.all():
        for value in payment.payment_values.all():
            register.amount += value.value
    register.save()
    

class PaymentsListCreateAPIView(APIView):

    def get(
        self,
        request: Request,
        gym_id: str,
        student_id: str
        ) -> Response:
        student = get_object_or_404(Student, id=student_id)
        student_payments = student.payments.all()
        serializer = PaymentSerializer(instance=student_payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(
        self,
        request: Request,
        gym_id: str,
        student_id: str
        ) -> Response:
        try:
            serializer = PaymentSerializer(data=request.data)
            serializer = build_payment_serializer(
                serializer=serializer,
                student_id=student_id
            )
            ic(serializer.initial_data)
            if serializer.is_valid():
                ic("valid")
                validate_payment_serializer(serializer=serializer, student_id=student_id)
                ic("custom valid")
                serializer.save()
                update_cash_register_amount(serializer.data["cash_register"])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomValidatorException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentDeleteAPIView(APIView):

    def delete(
        self,
        request: Request,
        gym_id: str,
        payment_id: str,
        student_id: str
        ) -> Response:
        try:    
            payment = get_object_or_404(Payment, id=payment_id)
            payment = validate_payment_deletion(payment)
            payment.delete()
            update_cash_register_amount(register_id=payment.cash_register.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentValuesListCreateAPIView(APIView):
    def get(
        self,
        request: Request,
        student_id: str,
        payment_id: str,
        gym_id: str
        ) -> Response:

        payment = get_object_or_404(Payment, id=payment_id)
        values = payment.payment_values.all()
        serializer = PaymentValueSerializer(instance=values, many=True)
        
        return Response(serializer.data)

    def post(
        self,
        request: Request,
        student_id: str,
        payment_id: str,
        gym_id: str
        ) -> Response:
        try:
            data = request.data
            payment = get_object_or_404(Payment, id=payment_id)
            serializer = PaymentValueSerializer(data=data)
            serializer = validate_payment_value_serializer(
                serializer=serializer,
                payment_id=payment_id
                )
            if serializer.is_valid():
                serializer.save()
                update_cash_register_amount(register_id=payment.cash_register.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentValueDeleteAPIView(APIView):
    def delete(
        self,
        request: Request,
        gym_id: str,
        student_id: str,
        payment_id: str,
        value_id: str
        ) -> Response:
        value = get_object_or_404(PaymentValue, id=value_id)
        value.delete()
        update_cash_register_amount(register_id=value.payment.cash_register.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from app.utils.exceptions import CustomValidatorException
from students.models import Student
from .models import Payment, PaymentValue
from .serializers import PaymentSerializer, PaymentValueSerializer, PaymentDetailSerializer
from .validators import validate_payment_deletion, validate_payment_value_serializer, validate_payment_serializer
from .serializer_builders import build_payment_serializer
from app.utils.paginator import paginate_serializer
from rest_framework.pagination import PageNumberPagination
from cash_registers.utils import update_cash_register_amount    
from app.utils.permissions import AllowRoles


class PaymentsListCreateAPIView(APIView):

    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def get(
        self,
        request: Request,
        student_id: int
        ) -> Response:
        gym_id = request.user.profile.gym.id
        student = get_object_or_404(Student, id=student_id)
        student_payments = student.payments.all().order_by('-next_payment_date')
        
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=student_payments,
            request=request,
            serializer=PaymentDetailSerializer,
            paginator=paginator
        )
        
        return paginator.get_paginated_response(serializer.data)

    def post(
        self,
        request: Request,
        student_id: int
        ) -> Response:
        try:
            gym_id = request.user.profile.gym.id
            serializer = PaymentSerializer(data=request.data)
            serializer = build_payment_serializer(
                serializer=serializer,
                student_id=student_id,
            )
            if serializer.is_valid():
                validate_payment_serializer(serializer=serializer, student_id=student_id)
                serializer.save()
                update_cash_register_amount(serializer.data["cash_register"])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailDeleteAPIView(APIView):
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowRoles(["staff", "manager"])]
        return [AllowRoles()]

    def get(
        self,
        request: Request,
        payment_id: int,
        student_id: int,
        ) -> Response:
        gym_id = request.user.profile.gym.id
        payment = get_object_or_404(Payment, id=payment_id)
        serializer = PaymentDetailSerializer(instance=payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(
        self,
        request: Request,
        payment_id: int,
        student_id: int
        ) -> Response:
        try:
            gym_id = request.user.profile.gym.id
            payment = get_object_or_404(Payment, id=payment_id)
            payment = validate_payment_deletion(payment)
            payment.delete()
            update_cash_register_amount(register_id=payment.cash_register.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentValuesListCreateAPIView(APIView):

    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def get(
        self,
        request: Request,
        student_id: int,
        payment_id: int,
        ) -> Response:
        gym_id = request.user.profile.gym.id
        payment = get_object_or_404(Payment, id=payment_id)
        values = payment.payment_values.all()
        
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=values,
            request=request,
            serializer=PaymentValueSerializer,
            paginator=paginator
        )
        
        return paginator.get_paginated_response(serializer.data)

    def post(
        self,
        request: Request,
        student_id: int,
        payment_id: int,
        ) -> Response:
        try:
            gym_id = request.user.profile.gym.id
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

    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]
    
    def delete(
        self,
        request: Request,
        student_id: int,
        payment_id: int,
        value_id: int
        ) -> Response:
        gym_id = request.user.profile.gym.id
        value = get_object_or_404(PaymentValue, id=value_id)
        value.delete()
        update_cash_register_amount(register_id=value.payment.cash_register.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentValuesDeleteAllAPIView(APIView):

    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def delete(
        self,
        request: Request,
        student_id: int,
        payment_id: int
        ) -> Response:
        gym_id = request.user.profile.gym.id
        payment = get_object_or_404(Payment, id=payment_id)
        values = payment.payment_values.all()
        if values:
            for value in values:
                value.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

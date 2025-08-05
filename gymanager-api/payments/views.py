from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from students.models import Student
from .serializers import PaymentSerializer
from django.utils import timezone
from icecream import ic


def validate_payment_serializer(serializer) -> Serializer:
    ic(serializer.validated_data)
    return serializer


class PaymentsListCreateAPIView(APIView):

    def get(self, request: Request, student_id: str) -> Response:
        student = get_object_or_404(Student, id=student_id)
        student_payments = student.payments.all()
        serializer = PaymentSerializer(instance=student_payments, many=True)
        return Response(serializer.data)


    def post(self, request: Request, student_id: str) -> Response:
        data = request.data
        serializer = PaymentSerializer(data=data)

        if serializer.is_valid():
            serializer = validate_payment_serializer(serializer)
            return Response({"message": "is valid"})

        else:
            return Response(serializer.errors)


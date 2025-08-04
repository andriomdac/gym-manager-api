from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PaymentMethod
from .serializers import PaymentMethodSerializer
from app.utils.exceptions import CustomValidatorException


def validate_payment_method(serializer: Serializer) -> Serializer:
    data = serializer.validated_data
    if PaymentMethod.objects.filter(name=data["name"]).exists():
        raise CustomValidatorException("payment method with same name already exists.")
    return serializer


class PaymentMethodListCreateAPIView(APIView):

    def get(self, request: Request) -> Response:
        methods = PaymentMethod.objects.all()
        serializer = PaymentMethodSerializer(instance=methods, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        try:
            data = request.data
            serializer = PaymentMethodSerializer(data=data)

            if serializer.is_valid():
                serializer = validate_payment_method(serializer)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

            return Response()
        except CustomValidatorException as e:
            return Response({"error": f"{e}"})


class PaymentMethodRetrieveUpdateDeleteAPIView(APIView):

    def get(self, request: Request, method_id: str) -> Response:
        return Response()

    def put(self, request: Request, method_id: str) -> Response:
        return Response()

    def delete(self, request: Request, method_id: str) -> Response:
        return Response()

from rest_framework.request import Request
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PaymentPackage
from .serializers import PaymentPackageSerializer
from app.utils.exceptions import CustomValidatorException
from .validators import validate_payment_package


class PaymentPackageListCreateAPIView(APIView):

    def get(self, request: Request) -> Response:
        packages = PaymentPackage.objects.all()
        serializer = PaymentPackageSerializer(instance=packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data
            serializer = PaymentPackageSerializer(data=data)

            if serializer.is_valid():
                serializer = validate_payment_package(serializer)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response()
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentPackageRetrieveUpdateDeleteAPIView(APIView):

    def get(self, request: Request, package_id: str) -> Response:
        package = get_object_or_404(PaymentPackage, id=package_id)
        serializer = PaymentPackageSerializer(instance=package)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, package_id: str) -> Response:
        package = get_object_or_404(PaymentPackage, id=package_id)
        package.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

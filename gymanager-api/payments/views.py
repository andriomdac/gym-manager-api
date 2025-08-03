from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .models import PaymentMethod
from .serializers import PaymentMethodSerializer


class PaymentMethodListCreateAPIView(APIView):

    def get(self, request: Request) -> Response:
        methods = PaymentMethod.objects.all().order_by("name")
        serializer = PaymentMethodSerializer(data=methods, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        return Response()


class PaymentMethodRetrieveUpdateDeleteAPIView(APIView):

    def get(self, request: Request, method_id: str) -> Response:
        return Response()

    def put(self, request: Request, method_id: str) -> Response:
        return Response()

    def delete(self, request: Request, method_id: str) -> Response:
        return Response()


class PaymentPackageListCreateAPIView(APIView):

    def get(self, request: Request) -> Response:
        return Response()

    def post(self, request: Request) -> Response:
        return Response()


class PaymentPackageRetrieveUpdateDeleteAPIView(APIView):

    def get(self, request: Request, package_id: str) -> Response:
        return Response()

    def put(self, request: Request, package_id: str) -> Response:
        return Response()

    def delete(self, request: Request, package_id: str) -> Response:
        return Response()

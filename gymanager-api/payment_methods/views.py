from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class PaymentMethodListCreateAPIView(APIView):

    def get(self, request: Request) -> Response:
        return Response()

    def post(self, request: Request) -> Response:
        return Response()


class PaymentMethodRetrieveUpdateDeleteAPIView(APIView):

    def get(self, request: Request, method_id: str) -> Response:
        return Response()

    def put(self, request: Request, method_id: str) -> Response:
        return Response()

    def delete(self, request: Request, method_id: str) -> Response:
        return Response()

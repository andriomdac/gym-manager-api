from rest_framework.request import Request
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PaymentMethod
from .serializers import PaymentMethodSerializer
from app.utils.exceptions import CustomValidatorException
from .validators import validate_payment_method
from app.utils.paginator import paginate_serializer
from rest_framework.pagination import PageNumberPagination
from app.utils.permissions import AllowRoles


class PaymentMethodListCreateAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowRoles(["staff", "manager"])]
        else:
            return [AllowRoles()]

    def get(self, request: Request) -> Response:
        methods = PaymentMethod.objects.all()
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=methods,
            request=request,
            serializer=PaymentMethodSerializer,
            paginator=paginator
        )
        
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        try:
            data = request.data
            serializer = PaymentMethodSerializer(data=data)

            if serializer.is_valid():
                serializer = validate_payment_method(serializer)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response()
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentMethodRetrieveUpdateDeleteAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowRoles(["staff", "manager"])]
        return [AllowRoles()]

    def get(self, request: Request, method_id: int) -> Response:
        method = get_object_or_404(PaymentMethod, id=method_id)
        serializer = PaymentMethodSerializer(instance=method)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, method_id: int) -> Response:
        method = get_object_or_404(PaymentMethod, id=method_id)
        method.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

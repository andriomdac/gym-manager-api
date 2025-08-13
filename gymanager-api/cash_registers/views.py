from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import CashRegisterSerializer, CashRegisterDetailSerializer
from .models import CashRegister


def validate_cash_resgister_serializer(serializer) -> Response:
    return serializer


class CashRegisterListCreate(APIView):

    def get(self, request: Request) -> Response:
        registers = CashRegister.objects.all()
        serializer = CashRegisterSerializer(instance=registers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        data = request.data
        serializer = CashRegisterSerializer(data=data)
        serializer = validate_cash_resgister_serializer(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CashRegisterClose(APIView):
    def post(self, request: Request, register_id: str) -> Response:
        register = get_object_or_404(CashRegister, id=register_id)
        serializer = CashRegisterSerializer(instance=register)

        if register.is_opened:
            register.is_opened = False
            register.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={"detail": "cash register already closed"}, status=status.HTTP_400_BAD_REQUEST)


class CashRegisterDetail(APIView):
    def get(self, request: Request, register_id: str) -> Response:
        register = get_object_or_404(CashRegister, id=register_id)
        serializer = CashRegisterDetailSerializer(instance=register)
        return Response(serializer.data, status=status.HTTP_200_OK)
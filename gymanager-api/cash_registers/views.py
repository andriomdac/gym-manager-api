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
from datetime import datetime
from app.utils.paginator import paginate_serializer
from rest_framework.pagination import PageNumberPagination
from .utils import build_cash_resgister_serializer
from app.utils.permissions import AllowRoles


class CashRegisterListCreate(APIView):
    
    def get_permissions(self):
        return [AllowRoles(["manager"])]

    def get(
        self,
        request: Request,
        gym_id: str,
        ) -> Response:
        registers = CashRegister.objects.filter(gym=gym_id).order_by('-register_date')
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=registers,
            request=request,
            serializer=CashRegisterSerializer,
            paginator=paginator
        )
        return paginator.get_paginated_response(serializer.data)

    def post(
        self,
        request: Request,
        gym_id: str,
        ) -> Response:
        data = request.data
        serializer = CashRegisterSerializer(data=data)
        serializer = build_cash_resgister_serializer(
            serializer_instance=serializer,
            gym_id=gym_id
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CashRegisterClose(APIView):

    def get_permissions(self):
        return [AllowRoles(["manager"])]
    
    def post(
        self,
        request: Request,
        gym_id: str,
        register_id: str
        ) -> Response:
        register = get_object_or_404(CashRegister, id=register_id)
        serializer = CashRegisterSerializer(instance=register)

        if register.is_opened:
            register.is_opened = False
            register.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={"detail": "cash register already closed"}, status=status.HTTP_400_BAD_REQUEST)


class CashRegisterDetail(APIView):

    def get_permissions(self):
        return [AllowRoles(["manager"])]

    def get(
        self,
        request: Request,
        gym_id: str,
        register_id: str
        ) -> Response:
        register = get_object_or_404(CashRegister, id=register_id)
        serializer = CashRegisterDetailSerializer(instance=register)
        return Response(serializer.data, status=status.HTTP_200_OK)
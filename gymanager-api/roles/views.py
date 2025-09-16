from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.utils.paginator import paginate_serializer
from rest_framework.pagination import PageNumberPagination
from .models import Role
from .serializers import RoleSerializer
from app.utils.permissions import AllowRoles

class RoleListCreateAPIView(APIView):

    def get_permissions(self):
        return [AllowRoles()]    

    def get(self, request: Request):
        queryset = Role.objects.all()
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=queryset,
            request=request,
            serializer=RoleSerializer,
            paginator=paginator
        )        
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

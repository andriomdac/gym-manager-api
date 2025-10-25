from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.request import Request
from .serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from app.utils.paginator import paginate_serializer
from app.utils.permissions import AllowRoles


class UserListCreateAPIView(APIView):
    
    def get_permissions(self):
        return [AllowRoles()]

    def get(self, request: Request):
        users = User.objects.all()
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=users,
            request=request,
            serializer=UserSerializer,
            paginator=paginator
            )
        return paginator.get_paginated_response(serializer.data)
        
        

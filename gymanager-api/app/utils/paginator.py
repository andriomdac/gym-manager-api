from typing import Any, Type
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.pagination import BasePagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    
    def get_paginated_response(self, data):
        page_number = self.page.number
        page_size = self.get_page_size(self.request)
        total_items = self.page.paginator.count
        total_pages = self.page.paginator.num_pages
        
        pagination_data = {
            'current_page': page_number,
            'per_page': page_size,
            'total_items': total_items,
            'total_pages': total_pages,
            'has_next_page': self.page.has_next(),
            'has_previous_page': self.page.has_previous(),
        }

        return Response({
            'results': data,
            'pagination': pagination_data
        })



def paginate_serializer(
    queryset: QuerySet[Any],
    request: Request,
    serializer: Type[Serializer],
    paginator: BasePagination,
) -> Serializer:
    paginated_queryset = paginator.paginate_queryset(queryset=queryset, request=request)
    return serializer(instance=paginated_queryset, many=True)



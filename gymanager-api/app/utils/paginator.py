from typing import Any, Type
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.pagination import BasePagination


def paginate_serializer(
    queryset: QuerySet[Any],
    request: Request,
    serializer: Type[Serializer],
    paginator: BasePagination,
) -> Serializer:
    paginated_queryset = paginator.paginate_queryset(queryset=queryset, request=request)
    return serializer(instance=paginated_queryset, many=True)

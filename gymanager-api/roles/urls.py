from django.urls import path
from .views import (
    RoleListCreateAPIView,
    )


urlpatterns = [
    path('', RoleListCreateAPIView.as_view(), name='role_list_create'),
]

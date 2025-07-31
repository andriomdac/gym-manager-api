from django.urls import path
from .views import (
    gym_list_create_view
)

urlpatterns = [
    path('', gym_list_create_view, name='gym_list_create'),
]
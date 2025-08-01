from django.urls import path
from .views import (
    GymListCreateAPIView,
    GymRetrieveUpdateDestroyAPIView
)


urlpatterns = [
    path('', GymListCreateAPIView.as_view(), name='gym_list_create'),
    path('<str:gym_id>/', GymRetrieveUpdateDestroyAPIView.as_view(), name='gym_retrieve_update_destroy')
]

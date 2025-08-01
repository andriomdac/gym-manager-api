from django.urls import path
from .views import (
    StudentListCreateAPIView,
    StudentRetrieveUpdateDestroyAPIView
)


urlpatterns = [
    path('', StudentListCreateAPIView.as_view(), name='student_list_create'),
    path('<str:student_id>/', StudentRetrieveUpdateDestroyAPIView.as_view(), name='student_retrieve_update_destroy')
]

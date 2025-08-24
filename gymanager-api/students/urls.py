from django.urls import path
from .views import (
    StudentListCreateAPIView,
    StudentRetrieveUpdateDestroyAPIView,
    StudentStatusListUpdateAPIView,
)


urlpatterns = [
    path('', StudentListCreateAPIView.as_view(), name='student_list_create'),
    path('status/', StudentStatusListUpdateAPIView.as_view(), name='student_list_update_status'),
    path('<str:student_id>/', StudentRetrieveUpdateDestroyAPIView.as_view(), name='student_retrieve_update_destroy')
]

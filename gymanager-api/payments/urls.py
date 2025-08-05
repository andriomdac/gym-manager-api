from django.urls import path
from .views import PaymentsListCreateAPIView

urlpatterns = [
    path('', PaymentsListCreateAPIView.as_view(), name="payment_list_create"),
]

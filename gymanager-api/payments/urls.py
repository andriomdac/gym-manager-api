from django.urls import path
from .views import PaymentsListCreateAPIView, PaymentDeleteAPIView

urlpatterns = [
    path('', PaymentsListCreateAPIView.as_view(), name="payment_list_create"),
    path('<str:payment_id>/', PaymentDeleteAPIView.as_view(), name='payment_delete'),
]

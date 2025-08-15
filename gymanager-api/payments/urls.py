from django.urls import path
from .views import (
    PaymentsListCreateAPIView,
    PaymentDeleteAPIView,
    PaymentValuesListCreateAPIView,
    PaymentValueDeleteAPIView,
    )

urlpatterns = [
    path('', PaymentsListCreateAPIView.as_view(), name="payment_list_create"),
    path('<str:payment_id>/', PaymentDeleteAPIView.as_view(), name='payment_delete'),
    path('<str:payment_id>/values/', PaymentValuesListCreateAPIView.as_view(), name='payment_value_list_create'),
    path('<str:payment_id>/values/<str:value_id>/', PaymentValueDeleteAPIView.as_view(), name='payment_value_delete' ),
]

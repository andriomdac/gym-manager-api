from django.urls import path
from .views import (
    PaymentsListCreateAPIView,
    PaymentDetailDeleteAPIView,
    PaymentValuesListCreateAPIView,
    PaymentValuesDeleteAllAPIView,
    PaymentValueDeleteAPIView,
    )

urlpatterns = [
    path('', PaymentsListCreateAPIView.as_view(), name="payment_list_create"),
    path('<str:payment_id>/', PaymentDetailDeleteAPIView.as_view(), name='payment_detail_delete'),
    path('<str:payment_id>/values/', PaymentValuesListCreateAPIView.as_view(), name='payment_value_list_create'),
    path('<str:payment_id>/values/delete/', PaymentValuesDeleteAllAPIView.as_view(), name='payment_values_delete_all'),
    path('<str:payment_id>/values/<str:value_id>/', PaymentValueDeleteAPIView.as_view(), name='payment_value_delete' ),
]

from django.urls import path
from .views import (
    PaymentMethodListCreateAPIView,
    PaymentMethodRetrieveUpdateDeleteAPIView
    )


urlpatterns = [
    path('', PaymentMethodListCreateAPIView.as_view(), name='payment_method_list_create'),
    path('<int:method_id>/', PaymentMethodRetrieveUpdateDeleteAPIView.as_view(), name='payment_method_retrieve_update_delete'),
]
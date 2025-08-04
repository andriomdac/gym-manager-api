from django.urls import path
from .views import (
    PaymentPackageListCreateAPIView,
    PaymentPackageRetrieveUpdateDeleteAPIView
    )


urlpatterns = [
    path('', PaymentPackageListCreateAPIView.as_view(), name='payment_package_list_create'),
    path('<str:package_id>/', PaymentPackageRetrieveUpdateDeleteAPIView.as_view(), name='payment_package_retrieve_update_delete'),
]
from django.urls import path
from .views import (
    CashRegisterListCreate,
    CashRegisterClose,
    )

urlpatterns = [
    path('', CashRegisterListCreate.as_view(), name='cash_register_list_create'),
    path('<str:register_id>/close/', CashRegisterClose.as_view(), name='cash_register_close'),
]
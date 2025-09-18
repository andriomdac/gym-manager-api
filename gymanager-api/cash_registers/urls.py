from django.urls import path
from .views import CashRegisterListCreate, CashRegisterClose, CashRegisterDetail


urlpatterns = [
    path(
        "",
        CashRegisterListCreate.as_view(),
        name="cash_register_list_create"
    ),
    path(
        "<int:register_id>/",
        CashRegisterDetail.as_view(),
        name="cash_register_detail"
    ),
    path(
        "<int:register_id>/close/",
        CashRegisterClose.as_view(),
        name="cash_register_close",
    ),
]


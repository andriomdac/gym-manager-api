from django.urls import path
from .views import CashRegisterListCreate, CashRegisterClose, CashRegisterDetail, CashRegisterListOpenRegistersOnly


urlpatterns = [
    path(
        "",
        CashRegisterListCreate.as_view(),
        name="cash_register_list_create"
    ),
    path(
        "list-open/",
        CashRegisterListOpenRegistersOnly.as_view(),
        name="cash_register_list_open_registers_only"
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


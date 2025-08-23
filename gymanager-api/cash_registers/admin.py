from django.contrib import admin
from .models import CashRegister


@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ["id", "gym", "created_at", "register_date", "is_opened", "amount",]

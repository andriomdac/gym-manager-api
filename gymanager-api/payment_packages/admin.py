from django.contrib import admin
from .models import PaymentPackage


@admin.register(PaymentPackage)
class PaymentPackageAdmin(admin.ModelAdmin):
    list_display = ["name", "duration_days",]  
from django.contrib import admin
from .models import Payment, PaymentValue


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'payment_date', 'next_payment_date', 'student', 'payment_package', 'cash_register', 'observations',]

@admin.register(PaymentValue)
class PaymentValueAdmin(admin.ModelAdmin):
    list_display = ['payment', 'payment_method', 'value',]


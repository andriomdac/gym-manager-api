from rest_framework import serializers
from .models import CashRegister
from payments.serializers import PaymentDetailSerializer
from payments.models import PaymentMethod

class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRegister
        fields = "__all__"


class CashRegisterDetailSerializer(CashRegisterSerializer):
    payments = serializers.SerializerMethodField()
    values_per_method = serializers.SerializerMethodField()

    def get_payments(self, obj):
        cash_register_payments = obj.payments.all()
        serializer = PaymentDetailSerializer(cash_register_payments, many=True)
        return serializer.data

    def get_values_per_method(self, obj):
        payments = obj.payments.all()
        total_values_per_method = {}
        for payment in payments:
            for value in payment.payment_values.all():
                if value.payment_method.name not in total_values_per_method:
                    total_values_per_method[value.payment_method.name] = 0
                total_values_per_method[value.payment_method.name] += value.value            
        return total_values_per_method

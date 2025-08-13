from rest_framework import serializers
from .models import CashRegister
from payments.serializers import PaymentDetailSerializer


class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRegister
        fields = "__all__"


class CashRegisterDetailSerializer(CashRegisterSerializer):
    payments = serializers.SerializerMethodField()

    def get_payments(self, obj):
        cash_register_payments = obj.payments.all()
        serializer = PaymentDetailSerializer(cash_register_payments, many=True)
        return serializer.data
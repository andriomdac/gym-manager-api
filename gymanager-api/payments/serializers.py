from rest_framework import serializers
from .models import Payment, PaymentValue


class PaymentValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentValue
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

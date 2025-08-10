from rest_framework import serializers
from .models import Payment, PaymentValue
from payment_packages.serializers import PaymentPackageSerializer

class PaymentValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentValue
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentListSerializer(PaymentSerializer):
    payment_package = PaymentPackageSerializer(read_only=True)

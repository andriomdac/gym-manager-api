from rest_framework import serializers
from .models import PaymentPackage


class PaymentPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPackage
        fields = "__all__"

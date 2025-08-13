from rest_framework import serializers
from .models import PaymentPackage


class PaymentPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPackage
        fields = "__all__"


class PaymentPackageSummarySerializer(PaymentPackageSerializer):
    class Meta:
        model = PaymentPackage
        fields = ["id", "name",]
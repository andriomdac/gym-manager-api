from rest_framework import serializers
from .models import Payment
from payment_packages.serializers import PaymentPackageSummarySerializer
from students.serializers import StudentSummarySerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentDetailSerializer(PaymentSerializer):
    student = StudentSummarySerializer(read_only=True)
    payment_package = PaymentPackageSummarySerializer(read_only=True)
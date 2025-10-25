from rest_framework import serializers
from .models import Payment, PaymentValue
from payment_packages.serializers import PaymentPackageSummarySerializer
from students.serializers import StudentSummarySerializer
from icecream import ic

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class PaymentValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentValue
        fields = "__all__"

class PaymentDetailSerializer(PaymentSerializer):
    student = StudentSummarySerializer(read_only=True)
    payment_package = PaymentPackageSummarySerializer(read_only=True)
    payment_values = serializers.SerializerMethodField()

    def get_payment_values(self, obj):
        return [
            {
                "id": value.id,
                "method": value.payment_method.name,
                "value": value.value
            }
            for value in obj.payment_values.all()
        ]

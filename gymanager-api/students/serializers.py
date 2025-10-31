from datetime import datetime
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from .models import Student, StudentStatus
from icecream import ic


class StudentSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = "__all__"


    def get_is_overdue(self, obj):
        today = datetime.today().date()
        last_payment = obj.payments.all().order_by("-next_payment_date").first()
        if last_payment is None:
            return True

        if last_payment.next_payment_date < today:
            return True
        return False

class StudentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name",]


class StudentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStatus
        fields = ["student", "is_overdue", "last_checked",]

from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from .models import Student, StudentStatus


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class StudentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name",]


class StudentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStatus
        fields = ["student", "is_overdue", "last_checked",]
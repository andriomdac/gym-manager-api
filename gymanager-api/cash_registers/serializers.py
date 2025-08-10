from rest_framework.serializers import ModelSerializer
from .models import CashRegister


class CashRegisterSerializer(ModelSerializer):
    class Meta:
        model = CashRegister
        fields = "__all__"
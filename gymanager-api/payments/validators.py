from datetime import datetime
from django.utils import timezone
from icecream import ic
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from app.utils.exceptions import CustomValidatorException
from cash_registers.models import CashRegister
from .serializers import PaymentSerializer, PaymentValueSerializer
from .utils import get_next_payment_date
from .models import Payment
from payment_methods.models import PaymentMethod
from students.models import Student


def validate_payment_serializer(serializer: Serializer, student_id: str) -> Serializer:
    data = serializer.validated_data
    cash_register = data["cash_register"]
    
    if cash_register.payments.filter(student=data["student"]).exists():
        raise CustomValidatorException(
            "Já existe um pagamento deste aluno neste caixa."
        )
    if not cash_register.is_opened:
        raise CustomValidatorException("Não é possível adicionar novo pagamento a um caixa fechado.")


def validate_payment_deletion(payment: Payment) -> Payment:
    """
    It checks whether the payment is in a opened cash register or not.
    -> If so, it's possible to be deleted, it's not otherwise.
    """
    if payment.cash_register.is_opened:
        return payment
    else:
        raise CustomValidatorException(
            "Não é mais possível excluir este pagamento, pois seu caixa já está fechado."
            )


def validate_payment_value_serializer(
    serializer: Serializer,
    payment_id: str
    ) -> Serializer:
    data = serializer.initial_data
    data["payment"] = payment_id
    payment = get_object_or_404(Payment, id=payment_id)
    
    if data.get("payment_method") and data.get("value"):
        method = get_object_or_404(PaymentMethod, id=data["payment_method"])
        
        if not payment.cash_register.is_opened:
            raise CustomValidatorException("Não é mais possível modificar este pagamento, pois seu caixa já está fechado.")
            
        if payment.payment_values.filter(payment_method=data["payment_method"]).exists():
            raise CustomValidatorException(f"O método {method.name} já existe para este pagamento.")
    else:
        raise CustomValidatorException("Método de pagamento e/ou Valor Recebido não pode(m) estar vazio(s)")

    new_serializer = PaymentValueSerializer(data=data)
    return new_serializer

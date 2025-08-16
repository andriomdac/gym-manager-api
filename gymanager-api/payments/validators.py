from datetime import datetime
from django.utils import timezone
from icecream import ic
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer
from app.utils.exceptions import CustomValidatorException
from cash_registers.models import CashRegister
from .serializers import PaymentSerializer, PaymentValueSerializer
from .utils import get_next_payment_date
from .models import Payment
from payment_methods.models import PaymentMethod
from students.models import Student


def validate_payment_serializer(serializer: Serializer, student_id: str) -> Serializer:
    """
    Validates and prepares payment data before saving.

    This function performs a series of checks to ensure the payment is valid,
    including cash register status, payment date rules, and preventing
    duplicate payments. It also calculates the next payment date.

    Args:
        serializer: The DRF serializer instance with initial data.
        student_id: The ID of the student making the payment.

    Returns:
        An instance of PaymentSerializer with validated and prepared data.
    
    Raises:
        CustomValidatorException: If any validation rule is not met.
    """
    data = serializer.initial_data
    if "cash_register" in data:
        cash_register = get_object_or_404(CashRegister, id=data["cash_register"])
    else:
        raise CustomValidatorException("'cash_register' field not found")

    student = get_object_or_404(Student, id=student_id)
    today = timezone.localdate()
    data["student"] = student_id

    last_payment = student.payments.order_by("next_payment_date").last()
    if last_payment:
        if today < last_payment.next_payment_date:
            data["payment_date"] = last_payment.next_payment_date
    else:
        data["payment_date"] = today

    if cash_register.payments.filter(student=data["student"]).exists():
        raise CustomValidatorException(
            "there is already a payment of this student in this cash register"
        )

    data["next_payment_date"] = get_next_payment_date(
        payment_date=data["payment_date"],
        payment_package_id=data["payment_package"]
    )

    if not cash_register.is_opened:
        raise CustomValidatorException("cannot add new payment to a closed cash register.")

    return PaymentSerializer(data=data)


def validate_payment_deletion(payment: Payment) -> Payment:
    """
    It checks whether the payment is in a opened cash register or not.
    -> If so, it's possible to be deleted, it's not otherwise.
    """
    if payment.cash_register.is_opened:
        return payment
    else:
        raise CustomValidatorException(
            "cannot delete this payment anymore, because it's cash register is already closed"
            )


def validate_payment_value_serializer(
    serializer: Serializer,
    payment_id: str
    ) -> Serializer:
    data = serializer.initial_data
    data["payment"] = payment_id
    payment = get_object_or_404(Payment, id=payment_id)
    
    if "payment_method" in data:
        method = get_object_or_404(PaymentMethod, id=data["payment_method"])
        if payment.payment_values.filter(payment_method=data["payment_method"]).exists():
            raise CustomValidatorException(f"method {method.name} already exists for this payment.")

    new_serializer = PaymentValueSerializer(data=data)
    return new_serializer
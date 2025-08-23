from django.utils import timezone
from rest_framework.serializers import Serializer
from rest_framework.generics import get_object_or_404
from students.models import Student
from payments.utils import get_next_payment_date
from payments.serializers import PaymentSerializer
from app.utils.exceptions import CustomValidatorException
from cash_registers.models import CashRegister


def build_payment_serializer(serializer: Serializer, student_id: str) -> Serializer:
    data = serializer.initial_data
    student = get_object_or_404(Student, id=student_id)
    today = timezone.localdate()
    data["student"] = student_id

    last_payment = student.payments.order_by("next_payment_date").last()
    if last_payment:
        if today < last_payment.next_payment_date:
            # Prevent overlapping payments:
            # If the previous payment is still active, 
            # schedule the new one to start when it expires.
            data["payment_date"] = last_payment.next_payment_date
    else:
        # No previous payments -> this is the first one
        data["payment_date"] = today

    if not "cash_register" in data:
        try:
            register = CashRegister.objects.get(register_date=today)
            data["cash_register"] = register.id        
        except CashRegister.DoesNotExist:
            raise CustomValidatorException("There isn't a cash register for today. Please create one")


    data["next_payment_date"] = get_next_payment_date(
        payment_date=data.get("payment_date"),
        payment_package_id=data.get("payment_package")
    )

    return PaymentSerializer(data=data)
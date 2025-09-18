from datetime import datetime, timedelta
from rest_framework.generics import get_object_or_404
from payment_packages.models import PaymentPackage
from app.utils.exceptions import CustomValidatorException


def get_next_payment_date(payment_date: datetime, payment_package_id: str) -> datetime:
    if not payment_package_id:
        raise CustomValidatorException("Campo 'payment_package' obrigatório.")

    payment_package = get_object_or_404(PaymentPackage, id=payment_package_id)
    return payment_date + timedelta(days=payment_package.duration_days)

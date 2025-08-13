# Standard library imports
from datetime import datetime, timedelta

# Third-party imports
from rest_framework.generics import get_object_or_404

# Local application imports
from payment_packages.models import PaymentPackage


def get_next_payment_date(payment_date: datetime, payment_package_id: str) -> datetime:
    payment_package = get_object_or_404(PaymentPackage, id=payment_package_id)
    return payment_date + timedelta(days=payment_package.duration_days)

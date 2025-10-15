from ._base import BASE_URL
from frontend.utils.http import build_api_headers
import requests as rq


class PaymentAPIClient:

    def __init__(self, student_id) -> None:
        self._base_url = f"{BASE_URL}/students/{student_id}/payments"

    def add_payment(self, request, payment_package_id):
        data = {"payment_package": payment_package_id}
        return rq.api.post(
            url=f"{self._base_url}/",
            headers=build_api_headers(request),
            json=data
        )

class PaymentPackageAPIClient:

    def __init__(self) -> None:
        self._base_url = f"{BASE_URL}/payment-packages"

    def list_packages(self, request):
        return rq.api.get(
            url=f"{self._base_url}/",
            headers=build_api_headers(request)
        )

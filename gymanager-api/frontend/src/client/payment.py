from django.contrib import messages
from ._base import BASE_URL
from frontend.utils.http import build_api_headers
import requests as rq
from icecream import ic


class PaymentAPIClient:

    def __init__(self, student_id) -> None:
        self._base_url = f"{BASE_URL}/students/{student_id}/payments"


    def list_payments(self, request):
        return rq.api.get(
            url=f"{self._base_url}/",
            headers=build_api_headers(request)
        )

    def add_payment(
        self,
        request,
        payment_package,
        cash_register
    ):
        data = {
            "payment_package": payment_package,
        }
        if cash_register:
            data["cash_register"] = cash_register
        return rq.api.post(
            url=f"{self._base_url}/",
            json=data,
            headers=build_api_headers(request)
        )

    def add_value(self, request, payment_id, value, payment_method):
        data = {
            "value": value,
            "payment_method": payment_method
        }
        return rq.api.post(
            url=f"{self._base_url}/{payment_id}/values/",
            headers=build_api_headers(request),
            json=data
        )

    def delete_value(self, request, payment_id, value_id):
        ic(value_id)
        return rq.api.delete(
            url=f"{self._base_url}/{payment_id}/values/{value_id}/",
            headers=build_api_headers(request)
        )

    def detail_payment(self, request, payment_id):
        return rq.api.get(
            url=f"{self._base_url}/{payment_id}/",
            headers=build_api_headers(request)
        )


class PaymentPackageAPIClient:

    def __init__(self) -> None:
        self._base_url = f"{BASE_URL}/payment-packages"

    def list_packages(self, request):
        return rq.api.get(
            url=f"{self._base_url}/",
            headers=build_api_headers(request)
        )


class PaymentMethodAPIClient:

    def __init__(self) -> None:
        self._base_url = f"{BASE_URL}/payment-methods"


    def list_methods(self, request):
        return rq.api.get(
            url=f"{self._base_url}/",
            headers=build_api_headers(request)
        )

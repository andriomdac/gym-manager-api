from frontend.src.client._base import BASE_URL
from frontend.utils.http import build_api_headers
import requests as rq
from icecream import ic



class StudentAPIClient:

    def __init__(self) -> None:
        self._base_url = f"{BASE_URL}/students"

    def add_student(
        self,
        request,
        name: str,
        phone: str,
        reference: str
    ):
        data = {
            "name": name,
            "phone": phone,
            "reference": reference
        }
        return rq.api.post(
            url=f"{self._base_url}/",
            json=data,
            headers=build_api_headers(request=request)
        )

    def list_students_paginated(self, request, page: int):
        return rq.api.get(
            url=f"{self._base_url}/?page={page}",
            headers=build_api_headers(request=request)
        )
    
    def detail_student(self, request, student_id):
        return rq.api.get(
            url = f"{self._base_url}/{student_id}",
            headers=build_api_headers(request)
        )

    def add_payment(
        self,
        request,
        payment_package,
        student_id
    ):
        data = {"payment_package": payment_package}
        return rq.api.post(
            url=f"{self._base_url}/{student_id}/payments/",
            json=data,
            headers=build_api_headers(request)
        )

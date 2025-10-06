from frontend.src.client._base import BASE_URL
from frontend.utils.http import build_api_headers
import requests as rq



class StudentAPIClient:

    def __init__(self, request) -> None:
        self._base_url = f"{BASE_URL}/students"
        self._request = request

    def add_student(
        self,
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
            headers=build_api_headers(self._request)
        )

    def list_students(self):
        return None

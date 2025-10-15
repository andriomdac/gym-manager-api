import requests as rq
from ._base import BASE_URL
from frontend.utils.http import build_api_headers


class RegisterAPIClient:

    def __init__(self) -> None:
        self._base_url = f"{BASE_URL}/cash-registers"


    def list_registers(self, request):
        return rq.api.get(
            url = f"{self._base_url}/",
            headers=build_api_headers(request)
        )

    def open_register(self, request, register_date=None):
        data = {}
        if register_date:
            data['register_date'] = register_date
        return rq.api.post(
            url=f"{self._base_url}/",
            headers=build_api_headers(request),
            json=data
        )
    
    def detail_register(self, request, register_id):
        return rq.api.get(
            url=f"{self._base_url}/{register_id}/",
            headers=build_api_headers(request),
        )

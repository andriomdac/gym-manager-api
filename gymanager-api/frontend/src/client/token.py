import requests as rq
from ._base import BASE_URL


class TokenAPIClient:
    def __init__(self) -> None:
        self._base_url = f"{BASE_URL}/token"

    def get_token(self, username: str, password: str):
        return rq.api.post(
            url=f"{self._base_url}/", json={"username": username, "password": password}
        )

    def verify_token(self, access_token: str):
        return rq.api.post(
            url=f"{self._base_url}/verify/", json={"token": access_token}
        )

    def refresh_token(self, refresh_token: str):
        return rq.api.post(
            url=f"{self._base_url}/refresh/", json={"refresh": refresh_token}
        )

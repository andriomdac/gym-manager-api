from src.client.token import TokenAPIClient
import streamlit as st
from utils.exceptions import CustomLoginException, SessionExpiredException


class Session:
    def __init__(self) -> None:
        pass

    def get_login_access(self, username: str, password: str):
        client = TokenAPIClient()
        response = client.get_token(username=username, password=password)
        if response.status_code == 200:
            st.session_state["access_token"] = response.json()["access"]
            st.session_state["refresh_token"] = response.json()["refresh"]
            st.rerun()
        elif response.status_code == 401:
            raise CustomLoginException(f"{response.json()['detail']}")
        elif response.status_code == 400:
            raise CustomLoginException("Por favor, forneça um usuário e senha válidos.")
        else:
            raise CustomLoginException("Erro desconhecido.")

    def access_token_is_valid(self, access_token: str):
        client = TokenAPIClient()
        response = client.verify_token(access_token=access_token)
        if response.status_code == 200:
            return True
        return False

    def update_session_tokens_by(self, new_access_tk: str):
        st.session_state["access_token"] = new_access_tk
        st.rerun()

    def refresh_token_session(self, refresh: str):
        client = TokenAPIClient()
        refresh = st.session_state["refresh_token"]
        response = client.refresh_token(refresh_token=refresh)

        if response.status_code == 200:
            self.update_session_tokens_by(
                new_access_tk=response.json()["access"],
            )
        else:
            raise SessionExpiredException("Erro ao atualizar sessão.")

    def clean_session(self):
        if "access_token" in st.session_state:
            del st.session_state["access_token"]
        if "refresh_token" in st.session_state:
            del st.session_state["refresh_token"]
        st.rerun()

    def validate_session(self):
        if "access_token" in st.session_state:
            token = st.session_state["access_token"]
            try:
                if not self.access_token_is_valid(access_token=token):
                    self.refresh_token_session(
                        refresh=st.session_state["refresh_token"]
                    )
            except SessionExpiredException:
                self.clean_session()

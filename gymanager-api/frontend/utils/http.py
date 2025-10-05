import streamlit as st


def build_api_headers() -> dict:
    access_token = st.session_state.get("access_token")
    return {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json" 
            }

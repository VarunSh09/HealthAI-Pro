import requests
import streamlit as st

from utils.session import (
    save_token,
    clear_token
)

API_BASE = "http://127.0.0.1:5000"


def login_user(email, password):
    response = requests.post(
        f"{API_BASE}/login",
        json={
            "email": email,
            "password": password
        }
    )

    return response


def register_user(payload):
    response = requests.post(
        f"{API_BASE}/register",
        json=payload
    )

    return response


def get_profile(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{API_BASE}/profile",
        headers=headers
    )

    return response


def logout():
    
    clear_token()

    keys = list(
        st.session_state.keys()
    )

    for key in keys:
        del st.session_state[key]

    st.query_params.clear()

    st.rerun()
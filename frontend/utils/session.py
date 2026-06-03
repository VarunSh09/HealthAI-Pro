from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st

cookies = EncryptedCookieManager(
    prefix="healthai_",
    password="super-secret-password"
)

if not cookies.ready():
    st.stop()


def save_token(token):

    cookies["token"] = token

    cookies.save()


def load_token():

    return cookies.get("token")


def clear_token():

    cookies["token"] = ""

    cookies.save()
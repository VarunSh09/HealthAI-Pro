import streamlit as st


def require_auth():

    if "token" not in st.session_state:
        st.switch_page("app.py")

    if not st.session_state.token:
        st.switch_page("app.py")


def get_current_user():
    return st.session_state.get(
        "user_data",
        {}
    )
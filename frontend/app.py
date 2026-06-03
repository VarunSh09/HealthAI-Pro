import streamlit as st
from components.ui import inject_custom_css, render_footer

from utils.auth import (
    login_user,
    register_user,
    get_profile,
    logout
)

import requests
import webbrowser
import datetime

from utils.session import (
    save_token,
    load_token
)


# 1. GLOBAL SETTINGS
# This must be the first Streamlit command in the script
st.set_page_config(
    page_title="HealthAI Pro Portal", 
    page_icon="🩺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS globally
inject_custom_css()

# =========================
# AUTH SYSTEM
# =========================



# -------------------------
# INIT SESSION STATE
# -------------------------

if "token" not in st.session_state:
    st.session_state.token = None

if "user_data" not in st.session_state:
    st.session_state.user_data = None


# -------------------------
# RESTORE TOKEN FROM COOKIE
# -------------------------

saved_token = load_token()
if saved_token == "":
    saved_token = None
if (
    saved_token
    and not st.session_state.token
):

    st.session_state.token = saved_token

    try:

        profile_res = get_profile(
            saved_token
        )

        if profile_res.status_code == 200:

            st.session_state.user_data = (
                profile_res.json()
            )

        else:

            st.session_state.token = None
            st.session_state.user_data = None

    except Exception:

        st.session_state.token = None
        st.session_state.user_data = None


# -------------------------
# PROFILE RECOVERY
# -------------------------

if (
    st.session_state.token
    and not st.session_state.user_data
):

    try:

        profile_res = get_profile(
            st.session_state.token
        )

        if profile_res.status_code == 200:

            st.session_state.user_data = (
                profile_res.json()
            )

        else:

            st.session_state.token = None
            st.session_state.user_data = None

    except Exception:

        st.session_state.token = None
        st.session_state.user_data = None


# -------------------------
# OAUTH REDIRECT HANDLING
# -------------------------

query_params = st.query_params

if "token" in query_params:

    token = query_params["token"]

    st.session_state.token = token

    save_token(token)

    try:

        profile_res = get_profile(token)

        if profile_res.status_code == 200:

            st.session_state.user_data = (
                profile_res.json()
            )

    except Exception:
        pass

    st.query_params.clear()

    st.rerun()




#public Navigation
if not st.session_state.token:

    public_pg = st.navigation({
    "Public": [
        st.Page(
            "public/Home_Public.py",
            title="Home",
            icon="🏠",
            default=True
        ),
        st.Page(
            "public/Login.py",
            title="Login",
            icon="🔐"
        ),
        st.Page(
            "public/Register.py",
            title="Register",
            icon="📝"
        ),
    ],
    "About Us": [
        st.Page("public/About.py", title="About HealthAI Pro", icon="ℹ️"),
    ]

})

    public_pg.run()
    st.stop()

    


# 3. NAVIGATION DEFINITION
# We define the pages and their labels for the sidebar
pg = st.navigation({
    "Overview": [
        st.Page("pages/Home.py",title="Welcome Home",icon="🏠",default=True),
        st.Page("pages/Dashboard.py", title="Live Dashboard", icon="📊"),
    ],
    "Clinical Tools": [
        st.Page("pages/Predictor.py", title="Disease Predictor", icon="🔍"),
        st.Page("pages/Health_Bot.py", title="Medical AI Chat", icon="💬"),
    ],
    "Insights & Admin": [ st.Page( "pages/Analytics.py", title="Advanced Analytics", icon="📈" ),
                          st.Page( "pages/History.py", title="Prediction History", icon="📜" ),
                            st.Page( "pages/Users.py", title="User Profile", icon="👤" ),
                             st.Page("pages/Admin.py",title="Admin Panel",icon="🛡️"), ],
    "About Us": [
        st.Page("pages/About.py", title="About HealthAI Pro", icon="ℹ️"),
    ]
})

# 4. RUN NAVIGATION
# This command actually renders the selected page

if st.sidebar.button("🚪 Logout", use_container_width=True):
    
    logout()
    st.session_state.token = None
    st.session_state.user_data = None
    save_token("")
    st.success("Logged out successfully")
    st.rerun()
pg.run()

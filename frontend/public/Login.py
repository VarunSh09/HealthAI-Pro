import streamlit as st
import webbrowser

from utils.auth import login_user, get_profile
from utils.session import save_token
from components.ui import inject_custom_css

# Page configuration for a professional feel
st.set_page_config(page_title="HealthAI Pro | Login", page_icon="🔐", layout="centered")

inject_custom_css()

# Custom CSS for the login container and buttons
st.markdown("""
    <style>
    /* Center the title */
    .title-text {
        text-align: center;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .subtitle-text {
        text-align: center;
        color: #6B7280;
        margin-bottom: 30px;
    }
    /* Style the divider */
    .divider {
        margin: 20px 0;
        text-align: center;
        border-bottom: 1px solid #ddd;
        line-height: 0.1em;
    }
    .divider span {
        background: #fff;
        padding: 0 10px;
        color: #999;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Login Container
# Using columns to create a "Card" effect in the center
_, col2, _ = st.columns([1, 2, 1])

with col2:
    st.markdown('<h1 class="title-text">🔐 HealthAI Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Welcome back! Please enter your details.</p>', unsafe_allow_html=True)

    with st.container(border=True):
        email = st.text_input("Email", placeholder="name@company.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        st.write("") # Spacer
        
        if st.button("Sign In", use_container_width=True, type="primary"):
            if email and password:
                response = login_user(email, password)

                if response.status_code == 200:
                    data = response.json()
                    token = data["access_token"]

                    st.session_state.token = token
                    save_token(token)

                    profile_res = get_profile(token)
                    if profile_res.status_code == 200:
                        st.session_state.user_data = profile_res.json()

                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.warning("Please fill in all fields")

    # Social Login Divider
    st.markdown('<div class="divider"><span>OR</span></div>', unsafe_allow_html=True)

    if st.button("Continue with Google", use_container_width=True):
        # Note: webbrowser.open works on the server/local machine, 
        # but in a hosted environment, consider using a link component.
        webbrowser.open("http://127.0.0.1:5000/google/login")

    st.write("")
    st.caption("By signing in, you agree to our Terms of Service and Privacy Policy.")
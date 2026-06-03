import webbrowser

import streamlit as st
import sys
import os
from datetime import datetime, time

# Path setup and imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.auth import logout
from utils.guards import require_auth, get_current_user
from components.ui import inject_custom_css, render_footer

# 1. Page Config & Security
st.set_page_config(page_title="User Profile", layout="wide", page_icon="👤")
inject_custom_css()
require_auth()

user = get_current_user() or {}

# Custom CSS for better card aesthetics
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    .profile-header {
        background: linear-gradient(90deg, #2B7CFF 0%, #0045B5 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .stat-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #f0f2f6;
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Hero Header
st.markdown(f"""
    <div class="profile-header">
        <h1>Welcome, {user.get("username", "User")}!</h1>
        <p>Manage your account settings and view your clinical access levels below.</p>
    </div>
""", unsafe_allow_html=True)

# 3. Main Layout
col_sidebar, col_main = st.columns([1, 3], gap="large")

with col_sidebar:
    # Profile Photo / Avatar placeholder
    initials = user.get("username", "U")[0].upper() if user.get("username") else "U"
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; padding: 20px; background: white; border-radius: 15px; border: 1px solid #E6E9EF;">
            <div style="width: 120px; height: 120px; border-radius: 50%; background: #E6F0FF; color: #2B7CFF; display: flex; align-items: center; justify-content: center; font-size: 48px; font-weight: bold; margin-bottom: 15px; border: 3px solid #2B7CFF;">
                {initials}
            </div>
            <h3 style="margin-bottom: 0;">{user.get("username", "User")}</h3>
            <p style="color: #666; font-size: 0.9rem;">{user.get("email", "No email provided")}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Spacer
    
    # Quick Actions
    with st.container(border=True):
        st.markdown("**Quick Actions**")
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            logout()
        if st.button("📧 Contact Support", use_container_width=True):
            st.toast("Redirecting to support...")
            webbrowser.open("mailto:support@healthai.com")

with col_main:
    # Stats Row
    stat1, stat2, stat3 = st.columns(3)
    stat1.metric("Account Type", "Authorized")
    stat2.metric("Access Level", f"Level {user.get('access_level', '1')}")
    stat3.metric("Status", "Active", delta="Verified")

    st.divider()

    # Detailed Info Tabs
    tab1, tab2 = st.tabs(["📋 General Information", "🛡️ Security & Access"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Username", value=user.get("username", ""), disabled=True)
            st.text_input("Email Address", value=user.get("email", ""), disabled=True)
            st.text_input("Provider", value=user.get("provider", "Local").title(), disabled=True)
        with c2:
            st.text_input("Date of Birth", value=user.get("dob", "Not Set"), disabled=True)
            st.text_input("Gender", value=user.get("gender", "Not Specified"), disabled=True)
            st.text_input("Joined Date", value="May 2026", disabled=True)

    with tab2:
        st.info("Your account is secured with JWT Token-based authentication.")
        st.markdown("#### Permissions")
        
        # Access Matrix
        perms = {
            "View Records": True,
            "Edit Records": False,
            "Export Data": False,
            "System Configuration": False
        }
        
        for perm, has_access in perms.items():
            icon = "✅" if has_access else "❌"
            st.markdown(f"{icon} **{perm}**")
        
        st.caption("User ID: `{}`".format(user.get("id", "N/A")))

# 4. Footer
st.divider()
render_footer(user.get("email", ""))
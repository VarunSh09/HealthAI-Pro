import streamlit as st
from utils.guards import require_auth, get_current_user
from components.ui import inject_custom_css, render_footer
from components.weather_alert import render_weather_alert

# 1. Page Configuration
st.set_page_config(
    page_title="Clinical AI | Home",
    page_icon="🏥",
    layout="wide"
)
# 2. Styling & Auth
inject_custom_css()
require_auth()

user = get_current_user() or {}
username = user.get("username", "Healthcare Professional")
email = user.get("email", "")



# 3. Hero Section (Header)
st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #f8fafc 0%, #eff6ff 100%);
        padding: 40px;
        border-radius: 15px;
        border-left: 5px solid #2563EB;
        margin-bottom: 30px;
    ">
        <h1 style="margin:0; font-size:2.8rem; color:#1e293b;">
            Welcome back, <span style="color:#2563EB;">{username}</span> 👋
        </h1>
        <p style="font-size:1.2rem; color:#64748B; margin-top:10px;">
            Your AI-assisted clinical workstation is active. 
            Select a module below to begin your workflow.
        </p>
    </div>
""", unsafe_allow_html=True)

render_weather_alert()


# 4. Quick Actions Section
st.subheader("⚡ Quick Actions")
q1, q2, q3 = st.columns(3)

with q1:
    with st.container(border=True):
        st.markdown("### 🔍 **Diagnose**")
        st.caption("Run new AI-powered clinical predictions.")
        if st.button("Start New Diagnosis", use_container_width=True, type="secondary"):
            st.switch_page("pages/Predictor.py")

with q2:
    with st.container(border=True):
        st.markdown("### 📜 **History**")
        st.caption("Review and manage past patient records.")
        if st.button("View Records", use_container_width=True,type="secondary"):
            st.switch_page("pages/History.py")

with q3:
    with st.container(border=True):
        st.markdown("### 📊 **Analytics**")
        st.caption("Insights on clinical data and trends.")
        if st.button("Open Dashboard", use_container_width=True,type="secondary"):
            st.switch_page("pages/Analytics.py")

st.markdown("<br>", unsafe_allow_html=True)

# 5. System Status Overview
st.subheader("📌 System Status")
k1, k2, k3, k4 = st.columns(4)

# Helper function for pretty metric display
def draw_status_card(label, value, status_color="#10b981"):
    st.markdown(f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            text-align: center;
        ">
            <p style="color: #64748B; font-size: 0.9rem; margin-bottom: 5px;">{label}</p>
            <p style="color: {status_color}; font-size: 1.2rem; font-weight: bold; margin: 0;">{value}</p>
        </div>
    """, unsafe_allow_html=True)

with k1:
    draw_status_card("ML Engine", "● Online")
with k2:
    draw_status_card("Database", "PostgreSQL", "#2563EB")
with k3:
    draw_status_card("Auth Session", "Encrypted")
with k4:
    draw_status_card("Reporting", "PDF Engine Ready")

# 6. Footer
st.markdown("---")
render_footer(email)
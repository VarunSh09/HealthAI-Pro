import streamlit as st

from components.ui import (
    inject_custom_css,
    render_footer
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="About | HealthAI Pro",
    layout="wide"
)

inject_custom_css()

# =========================
# HERO SECTION
# =========================
st.title("ℹ️ About HealthAI Pro")

st.write("""
HealthAI Pro is an AI-powered healthcare platform developed
to assist users in disease prediction and medical recommendation
based on symptoms using Machine Learning techniques.
""")

st.info(
    "🩺 Machine Learning Based Healthcare Prediction and Recommendation System"
)

st.divider()

# =========================
# PROJECT INFORMATION
# =========================
c1, c2 = st.columns(2)

with c1:

    st.subheader("📌 Project Details")

    st.write("**Project Name:**")
    st.write("Machine Learning Based Healthcare Prediction and Recommendation System")

    st.write("**Application Name:**")
    st.write("HealthAI Pro")

    st.write("**Technology Stack:**")
    st.write(
        """
        - Python
        - Streamlit
        - Flask API
        - PostgreSQL
        - Machine Learning
        - JWT Authentication
        - Google OAuth
        """
    )

with c2:

    st.subheader("👨‍💻 Developer Information")

    st.write("**Developer Name:**")
    st.write("Varun Sharma")

    st.write("**Roll Number:**")
    st.write("17032249014")

    st.write("**Course:**")
    st.write("Bachelor of Technology (B.Tech)")

    st.write("**Domain:**")
    st.write("Artificial Intelligence & Healthcare")

    st.write("**Academic Session:**")
    st.write("2022 - 2026")

st.divider()

# =========================
# PROJECT OBJECTIVE
# =========================
st.subheader("🎯 Project Objective")

st.write("""
The objective of this project is to develop an intelligent
healthcare prediction system capable of analyzing patient
symptoms and predicting possible diseases using Machine
Learning algorithms.

The system also provides:
- Severity analysis
- Medical precautions
- AI-generated healthcare summaries
- Prediction history
- Clinical analytics dashboards
- PDF medical reports
""")

st.divider()

# =========================
# FOOTER
# =========================
render_footer("HealthAI Pro")
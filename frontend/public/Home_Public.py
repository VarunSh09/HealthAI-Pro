import streamlit as st
from components.ui import inject_custom_css

inject_custom_css()

st.markdown("""
<div class="stCard" style="padding:40px; text-align:center;">
    <h1 style="font-size:3.5rem; color:#2563EB;">🩺 HealthAI Pro</h1>
    <p style="font-size:1.2rem; color:#64748B;">
        AI-powered healthcare prediction, analytics, and clinical intelligence platform.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🚀 Key Features")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="stCard">
        <h3>🔍 Disease Prediction</h3>
        <p>Predict diseases from symptoms using ML models.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="stCard">
        <h3>📊 Health Analytics</h3>
        <p>Visualize disease trends and clinical insights.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="stCard">
        <h3>📄 Medical Reports</h3>
        <p>Generate downloadable diagnostic PDF reports.</p>
    </div>
    """, unsafe_allow_html=True)

st.info("Please login or register to access clinical tools.")
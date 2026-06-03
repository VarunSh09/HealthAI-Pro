import streamlit as st
import pandas as pd
import plotly.express as px
from components.ui import inject_custom_css, render_footer
from utils.api import get_user_analytics
from utils.guards import require_auth, get_current_user

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Clinical Intelligence",
    page_icon="📊",
    layout="wide"
)

inject_custom_css()

# Minimalist Styling
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 20px; }
    .stMetric { background-color: #f8f9fa; border: 1px solid #eee; padding: 15px; border-radius: 10px; }
    /* Fix for pie chart legend overlapping footer */
    .main-container { padding-bottom: 50px; }
    </style>
    """, unsafe_allow_html=True)

# =========================
# AUTH & DATA LOAD
# =========================
require_auth()
user = get_current_user() or {}

response = get_user_analytics(st.session_state.token)

if response.status_code == 200:
    df = pd.DataFrame(response.json())
else:
    st.error("Failed to load analytics.")
    st.stop()

if df.empty:
    st.warning("No data available.")
    st.stop()

# Data Cleaning
df["date"] = pd.to_datetime(df["date"])

# =========================
# HEADER
# =========================
st.markdown('<p class="main-title">📊 Clinical Intelligence Analytics</p>', unsafe_allow_html=True)

# =========================
# KPI CARDS (Confidence Removed)
# =========================
k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Total Predictions", len(df))
with k2:
    top_d = df["disease"].value_counts().idxmax() if "disease" in df.columns else "N/A"
    st.metric("Most Frequent Detection", top_d)
with k3:
    avg_severity = round(df["severity"].mean(), 1) if "severity" in df.columns else "N/A"
    st.metric("Avg. Severity Index", avg_severity)

st.write("---")

# =========================
# PIE CHART (PRIMARY)
# =========================
st.subheader("🥧 Disease Distribution Overview")

if "disease" in df.columns:
    pie_df = df["disease"].value_counts().reset_index()
    pie_df.columns = ["Disease", "Cases"]

    fig_pie = px.pie(
        pie_df, 
        names="Disease", 
        values="Cases", 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Layout adjustment: clean legend at bottom
    fig_pie.update_layout(
        margin=dict(l=20, r=20, t=20, b=100),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("No disease data found to display.")

# =========================
# RECENT ACTIVITY (HIDDEN BY DEFAULT)
# =========================
st.write("")
with st.expander("🕒 View Prediction History Log"):
    # Drop confidence if it exists to keep table focused
    recent_df = df.sort_values(by="date", ascending=False)
    if "confidence_score" in recent_df.columns:
        recent_df = recent_df.drop(columns=["confidence_score"])
    
    st.dataframe(
        recent_df, 
        use_container_width=True,
        hide_index=True
    )

# =========================
# FOOTER
# =========================
# Spacing to ensure content doesn't hit footer
st.markdown("<br><br>", unsafe_allow_html=True)
render_footer("") # Minimal footer without email as requested previously
import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #F5F9FF;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3 {
            color: #0F172A;
            font-weight: 800;
        }

        p {
            color: #475569;
        }

        .stCard {
            background: #FFFFFF;
            padding: 24px;
            border-radius: 20px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
            margin-bottom: 18px;
        }

        .stat-card {
            background: white;
            padding: 22px;
            border-radius: 18px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
            text-align: center;
        }

        .stat-card small {
            color: #64748B;
            font-weight: 600;
        }

        .stat-card h3 {
            margin-top: 8px;
            color: #2563EB;
        }

        div[data-testid="stButton"] button {
            border-radius: 12px;
            font-weight: 700;
            height: 45px;
        }

        div[data-testid="stDownloadButton"] button {
            border-radius: 12px;
            font-weight: 700;
            height: 45px;
        }

        div[data-testid="stMetric"] {
            background: white;
            padding: 18px;
            border-radius: 16px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        }

        section[data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }

        .footer {
            text-align: center;
            color: #64748B;
            font-size: 13px;
            padding-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)


def render_footer(email):
    st.markdown("---")
    st.markdown(
        f"""
        <div class="footer">
            © 2026 HealthAI Pro | Logged in as: <b>{email}</b>
        </div>
        """,
        unsafe_allow_html=True
    )
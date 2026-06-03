import datetime
import streamlit as st
from utils.auth import register_user
from components.ui import inject_custom_css

# Page setup
st.set_page_config(page_title="HealthAI Pro | Join", page_icon="📝", layout="centered")

inject_custom_css()

# Custom Styling
st.markdown("""
    <style>
    .auth-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .auth-header h1 {
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .auth-header p {
        color: #64748B;
        font-size: 1.1rem;
    }
    .section-title {
        color: #0F172A;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .or-divider {
        text-align: center;
        margin: 1.5rem 0;
        color: #94A3B8;
        font-size: 0.9rem;
        font-weight: 500;
        position: relative;
    }
    .or-divider::before, .or-divider::after {
        content: "";
        position: absolute;
        top: 50%;
        width: 40%;
        height: 1px;
        background-color: #E2E8F0;
    }
    .or-divider::before { left: 0; }
    .or-divider::after { right: 0; }
    
    /* Clean up form spacing */
    .stNumberInput, .stTextInput, .stDateInput, .stSelectbox {
        margin-bottom: 5px;
    }
    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Layout: Centered column
_, col_main, _ = st.columns([1, 4, 1])

with col_main:
    st.markdown("""
        <div class="auth-header">
            <h1>📝 Create Your Account</h1>
            <p>Join the future of clinical intelligence</p>
        </div>
    """, unsafe_allow_html=True)

    # Use a container for a "Card" look
    with st.container(border=True):
        st.markdown('<p class="section-title">Account Credentials</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", placeholder="johndoe123")
        with col2:
            email = st.text_input("Email Address", placeholder="name@example.com")
        
        password = st.text_input("Password", type="password", placeholder="Enter a secure password")

        st.write("") # Spacer
        st.markdown('<p class="section-title">Personal Details</p>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        with col3:
            dob = st.date_input(
                "Date of Birth",
                min_value=datetime.date(1950, 1, 1),
                max_value=datetime.date.today(),
                help="Used to calibrate health analytics."
            )
        with col4:
            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"],
                index=0
            )

        st.write("") # Spacer
        st.write("") # Spacer

        # Registration logic trigger
        if st.button("Create Account", use_container_width=True, type="primary"):
            if not username or not email or not password:
                st.error("Please fill in all required fields.")
            else:
                payload = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "dob": str(dob),
                    "gender": gender
                }

                with st.spinner("Establishing secure connection..."):
                    response = register_user(payload)
                    
                if response.status_code == 201:
                    st.success("✅ Registration successful! Redirecting to login...")
                    st.switch_page("public/Login.py") 
                else:
                    error_msg = response.json().get("error", "Registration failed")
                    st.error(f"❌ {error_msg}")
                    
        # Social login - Properly pulled out of the registration conditional block
        st.markdown('<div class="or-divider">OR</div>', unsafe_allow_html=True)

        st.link_button(
            "🔒 Signup with Google", 
            "http://127.0.0.1:5000/google/login", 
            use_container_width=True
        )

    # Navigation back to login
    st.write("")
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        if st.button("Already have an account? Login", use_container_width=True):
            st.switch_page("public/Login.py")
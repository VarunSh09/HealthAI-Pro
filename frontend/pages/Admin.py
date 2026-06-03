import streamlit as st
import pandas as pd
from utils.guards import require_auth, get_current_user
from utils.api import get_admin_users
from components.ui import inject_custom_css, render_footer

# 1. PAGE SETUP & SECURITY
st.set_page_config(page_title="Admin Panel | System Oversight", layout="wide", page_icon="🛡️")
inject_custom_css()
require_auth()

user = get_current_user() or {}

# Strict Role Check
if user.get("role") != "admin":
    st.error("### ⛔ Access Denied\nThis area is restricted to system administrators only.")
    if st.button("Return to Dashboard"):
        st.switch_page("pages/dashboard.py") # Adjust path as needed
    st.stop()

# 2. DATA FETCHING
@st.cache_data(ttl=300) # Cache admin data for 5 minutes
def fetch_users(token):
    res = get_admin_users(token)
    if res.status_code == 200:
        return res.json().get("users", [])
    return None

users_data = fetch_users(st.session_state.get("token"))

# 3. HEADER & STATS
st.title("🛡️ Admin Control Center")
st.markdown("Monitor system health and manage user permissions.")

if users_data is not None:
    df = pd.DataFrame(users_data)
    
    # Summary Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Accounts", len(df))
    m2.metric("Admins", len(df[df['role'] == 'admin']) if 'role' in df.columns else "N/A")
    m3.metric("System Status", "Healthy", delta="Online")
    m4.metric("Active Session", user.get("username", "Admin"), delta_color="off")

    st.divider()

    # 4. USER MANAGEMENT SECTION
    st.subheader("👥 User Management")
    
    # Filter Toolbar
    col_search, col_role, col_export = st.columns([2, 1, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Search by Name or Email", placeholder="Search...")
    
    with col_role:
        role_filter = st.multiselect("Filter Role", options=df['role'].unique() if 'role' in df.columns else [])

    # Filtering Logic
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df['username'].str.contains(search_query, case=False, na=False) | 
            filtered_df['email'].str.contains(search_query, case=False, na=False)
        ]
    if role_filter:
        filtered_df = filtered_df[filtered_df['role'].isin(role_filter)]

    # Display Data
    if not filtered_df.empty:
        # Styled Dataframe
        st.dataframe(
            filtered_df,
            use_container_width=True,
            column_config={
                "id": st.column_config.TextColumn("User ID"),
                "email": st.column_config.TextColumn("Email Address"),
                "role": st.column_config.SelectboxColumn(
                    "Account Type", 
                    options=["admin", "user", "visitor"],
                    required=True
                ),
                "is_active": st.column_config.CheckboxColumn("Status"),
            },
            hide_index=True
        )
        
        with col_export:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export CSV",
                data=csv,
                file_name='system_users.csv',
                mime='text/csv',
                use_container_width=True
            )
    else:
        st.info("No users match your current filters.")

    # 5. ADMIN LOGS / AUDIT TRAIL (Placeholder for future)
    with st.expander("📜 View Audit Logs"):
        st.caption("Last 5 Administrative Actions")
        st.code(f"""
        [2026-05-11] {user.get('username')} accessed Admin Panel
        [2026-05-10] System automatic backup completed
        [2026-05-09] New user registration: 'clinic_user_04'
        """)

else:
    st.error("Unable to retrieve user list. Please verify API connection.")

# 6. FOOTER
st.write("---")
render_footer(user.get("email", ""))
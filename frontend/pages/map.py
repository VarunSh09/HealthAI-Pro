import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests

# --- CONFIGURATION & STYLING ---
def apply_production_styles():
    st.markdown("""
        <style>
        .hospital-card {
            border-radius: 12px;
            padding: 20px;
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 15px;
            transition: transform 0.2s;
        }
        .hospital-card:hover {
            transform: translateY(-2px);
            border-color: #1f77b4;
        }
        .status-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            background-color: #e8f5e9;
            color: #2e7d32;
        }
        </style>
    """, unsafe_allow_html=True)

# --- DATA SERVICE LAYER (Simulating a Database) ---
class HospitalService:
    @staticmethod
    @st.cache_data
    def get_all_hospitals():
        # In production, replace with: return pd.read_sql("SELECT * FROM hospitals", engine)
        data = {
            'id': [1, 2, 3, 4, 5],
            'name': ['Star Super Speciality', 'Unity Critical Care', 'Guardian Ortho', 'PIMS', 'Johal Hospital'],
            'city': ['Jalandhar', 'Jalandhar', 'Jalandhar', 'Jalandhar', 'Jalandhar'],
            'dept': ['Surgery', 'Emergency', 'Orthopedics', 'General', 'Multi-Specialty'],
            'rating': [4.8, 4.5, 4.7, 4.2, 4.4],
            'lat': [31.3262, 31.3345, 31.3190, 31.2950, 31.3410],
            'lon': [75.5761, 75.5890, 75.5810, 75.6020, 75.5720],
            'is_open': [True, True, True, True, True]
        }
        return pd.DataFrame(data)

# --- GEOLOCATION SERVICE ---
class LocationService:
    @staticmethod
    def get_user_city():
        """Attempts to find user city via IP. Defaults to Jalandhar for demo."""
        try:
            # Production: Use a paid API like IPStack or AbstractAPI
            # response = requests.get('http://ip-api.com/json/').json()
            # return response.get('city', 'Jalandhar')
            return "Jalandhar"
        except Exception:
            return "Jalandhar"

# --- CORE LOGIC ---
def render_referral_system():
    apply_production_styles()
    
    st.title("🏥 SmartCare Referral Engine")
    
    # 1. Initialize Services
    hospitals = HospitalService.get_all_hospitals()
    city = LocationService.get_user_city()
    
    # 2. Logic: Map Prediction to Dept
    # We assume 'last_prediction' was saved in st.session_state during the ML step
    predicted_disease = st.session_state.get('last_prediction', 'Heart attack')
    
    mapping = {
        'Fungal infection': 'Dermatology',
        'Heart attack': 'Cardiology',
        'Arthritis': 'Orthopedics',
        'Pneumonia': 'Pulmonology'
    }
    required_dept = mapping.get(predicted_disease, 'General Medicine')

    # 3. Layout
    col_ui, col_map = st.columns([1, 1])

    with col_ui:
        st.subheader(f"Nearby Care for {predicted_disease}")
        st.caption(f"Showing specialists in **{city}**")

        # Filtering with multi-specialty backup
        results = hospitals[
            (hospitals['city'] == city) & 
            ((hospitals['dept'] == required_dept) | (hospitals['dept'] == 'Multi-Specialty'))
        ]

        if results.empty:
            st.warning("No specific specialist found. Showing General Hospitals.")
            results = hospitals[hospitals['city'] == city]

        for _, row in results.iterrows():
            st.markdown(f"""
                <div class="hospital-card">
                    <span class="status-badge">OPEN 24/7</span>
                    <h3 style="margin: 10px 0 5px 0;">{row['name']}</h3>
                    <p style="color: #666;">Specialty: {row['dept']} | ⭐ {row['rating']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Book Clinic Appointment", key=f"btn_{row['id']}"):
                st.balloons()
                st.success(f"Confirmed! {row['name']} has received your diagnostic report.")

    with col_map:
        st.subheader("Interactive Map")
        # Initialize Map
        m = folium.Map(location=[results['lat'].mean(), results['lon'].mean()], zoom_start=13)
        
        for _, row in results.iterrows():
            folium.Marker(
                [row['lat'], row['lon']],
                popup=f"<b>{row['name']}</b><br>Rating: {row['rating']}",
                icon=folium.Icon(color='blue', icon='plus', prefix='fa')
            ).add_to(m)
        
        st_folium(m, height=500, width=None, use_container_width=True)

# --- EXECUTION ---
if __name__ == "__main__":
    # Simulate a prediction for demo purposes
    if 'last_prediction' not in st.session_state:
        st.session_state['last_prediction'] = 'Arthritis'
        
    render_referral_system()
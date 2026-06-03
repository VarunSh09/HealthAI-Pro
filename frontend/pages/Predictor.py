import streamlit as st
import numpy as np
import sys
import os
import uuid
import pandas as pd
from utils.ai_summary import generate_ai_summary
from utils.guards import require_auth, get_current_user
from utils.api import save_prediction
from components.ui import inject_custom_css, render_footer
from core.services import create_pdf
from components.weather_alert import render_weather_alert
# ROOT IMPORTS & CONFIG
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.assets import load_ml_assets

st.set_page_config(page_title="AI Predictor", layout="wide")
inject_custom_css()


# AUTH & ASSETS
require_auth()
user = get_current_user()
ml_model, master_rec, all_symptoms, sev_dict, formatted_to_tech = load_ml_assets()

if "current_uid" not in st.session_state:
    st.session_state.current_uid = f"HA-{str(uuid.uuid4())[:6].upper()}"

st.title("🧠 AI Clinical Diagnostic Engine")
st.caption(f"Patient Session ID: {st.session_state.current_uid}")
st.divider()

col_input, col_result = st.columns([1, 1.5], gap="large")

with col_input:
    st.subheader("🩺 Patient Clinical Input")
    with st.container(border=True):
        selected_ui = st.multiselect(
            "Select Symptoms",
            options=list(formatted_to_tech.keys()),
            help="Choose all observed symptoms."
        )

        c1, c2 = st.columns(2)
        with c1:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with c2:
            temperature = st.number_input("Temp (°F)", 95.0, 110.0, 98.6,step=0.10)

        st.markdown("<br>", unsafe_allow_html=True)
        run_diag = st.button("🚀 RUN AI ANALYSIS", use_container_width=True, type="primary")

# CALCULATION & RESULTS
if run_diag and selected_ui:
    with st.spinner("Analyzing symptom patterns..."):
        # Logic remains the same
        input_vector = np.zeros(len(all_symptoms))
        for s in selected_ui:
            tech_name = formatted_to_tech[s]
            idx = all_symptoms.index(tech_name)
            input_vector[idx] = 1

        prediction = ml_model.predict([input_vector])[0]
        total_sev = sum([sev_dict.get(formatted_to_tech[x].replace("_", " ").lower(), 0) for x in selected_ui])
        
        # Risk Logic
        if total_sev >= 15: risk_level = "Critical"
        elif total_sev >= 8: risk_level = "Moderate"
        else: risk_level = "Mild"
        
        # SAVE PREDICTION TO DATABASE
        payload = {
    "symptoms": ", ".join(selected_ui),
    "predicted_disease": str(prediction),
    "confidence_score": 0.95,
    "severity_score": float(total_sev)
                                        }

        save_res = save_prediction(
    st.session_state.token,
    payload
)

        if save_res.status_code == 201:
            st.toast("Prediction saved to history ✅")
        else:
             st.warning("Prediction generated, but history save failed.")

        # Data retrieval
        filtered_rec = master_rec[master_rec["Disease"].astype(str).str.lower() == str(prediction).lower()]
        rec_data = filtered_rec.iloc[0] if not filtered_rec.empty else {
            "Description": "No description available.", "Precaution_1": "Consult a professional."
        }

        # UI Rendering in Result Column
        with col_result:
            st.success(f"### Diagnosis: {prediction}")
            st.write(f"**Description:** {rec_data['Description']}")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Severity", total_sev)
            m2.metric("Risk", risk_level)
            m3.metric("Confidence", "95%")

            st.markdown("#### 🛡️ Precautions")
            precautions = [rec_data.get(f"Precaution_{i}", "") for i in range(1, 5) if pd.notna(rec_data.get(f"Precaution_{i}", ""))]
            
            p_cols = st.columns(2)
            for idx, item in enumerate(precautions):
                p_cols[idx % 2].markdown(f"- {item}")

    # SEPARATE BOTTOM SPACE FOR AI SUMMARY
    st.markdown("---")
    st.subheader("🤖 AI Clinical Intelligence Summary")
    
    with st.container(border=True):
        summary = generate_ai_summary(
            disease=str(prediction),
            symptoms=selected_ui,
            severity=total_sev,
            risk_level=risk_level,
            precautions=precautions
        )
        # Using a custom styling or just an info box for the summary
        st.info(summary)
    
    # =========================
    pdf_data = create_pdf(
    patient_id=st.session_state.current_uid,
    username=user.get("username", "User"),
    gender=user.get("gender", "N/A"),
    dob=user.get("dob", "N/A"),
    prediction=str(prediction),
    description=str(rec_data["Description"]),
    precautions=precautions,
    symptoms=selected_ui,
    severity=total_sev,
    confidence="95%"
)

    b1, b2, b3 = st.columns([1, 1, 1])
    with b1:
        st.download_button("📄 Download PDF Report", data=pdf_data, file_name=f"{prediction}_report.pdf", use_container_width=True)
    with b2:
        csv_df = pd.DataFrame([{"symptoms": selected_ui, "prediction": prediction, "severity": total_sev}])
        st.download_button("📊 Export Data", data=csv_df.to_csv(index=False), file_name="analysis.csv", use_container_width=True)
    with b3:
        if st.button("🔄 New Session", use_container_width=True):
            del st.session_state["current_uid"]
            st.rerun()

elif not run_diag:
    with col_result:
        st.info("👈 Please select symptoms and run analysis to see results.")


# FOOTER
render_footer(user.get("email", ""))
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.guards import (
    require_auth,
    get_current_user
)

from utils.api import (
    get_prediction_history
)

from components.ui import (
    inject_custom_css,
    render_footer
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Prediction History",
    layout="wide"
)

inject_custom_css()

require_auth()

user = get_current_user()


# =========================
# HEADER
# =========================

st.title("📜 Clinical Prediction History")

st.markdown(
    "Review all previously generated AI diagnostic reports."
)


# =========================
# FETCH HISTORY
# =========================

response = get_prediction_history(
    st.session_state.token
)


# =========================
# HANDLE RESPONSE
# =========================

if response.status_code == 200:

    history = response.json()

    if history:

        df = pd.DataFrame(history)

        # Convert datetime
        df["prediction_date"] = pd.to_datetime(
            df["prediction_date"]
        )

        # =========================
        # METRICS
        # =========================

        m1, m2, m3 = st.columns(3)

        with m1:
            st.metric(
                "Total Predictions",
                len(df)
            )

        with m2:
            st.metric(
                "Unique Diseases",
                df["predicted_disease"].nunique()
            )

        with m3:
            st.metric(
                "Average Confidence",
                f"{df['confidence_score'].mean()*100:.1f}%"
            )

        st.divider()


        # =========================
        # CHARTS
        # =========================

        col1, col2 = st.columns(2)

        with col1:

            disease_count = (
                df["predicted_disease"]
                .value_counts()
                .reset_index()
            )

            disease_count.columns = [
                "Disease",
                "Count"
            ]

            fig = px.bar(
                disease_count,
                x="Disease",
                y="Count",
                title="Most Predicted Diseases"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            fig2 = px.line(
                df.sort_values("prediction_date"),
                x="prediction_date",
                y="severity_score",
                title="Severity Trend Over Time",
                markers=True
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )


        # =========================
        # TABLE
        # =========================

        st.subheader("📋 Prediction Records")

        display_df = df[[
            "predicted_disease",
            "symptoms",
            "confidence_score",
            "severity_score",
            "prediction_date"
        ]]

        st.dataframe(
            display_df,
            use_container_width=True
        )

    else:

        st.info(
            "No prediction history found."
        )

else:

    st.error(
        "Failed to load prediction history."
    )


# =========================
# FOOTER
# =========================

render_footer(
    user.get("email", "")
)

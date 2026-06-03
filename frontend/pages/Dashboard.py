import streamlit as st
import pandas as pd
import plotly.express as px

from utils.guards import require_auth, get_current_user
from components.ui import inject_custom_css, render_footer


# PAGE CONFIG
st.set_page_config(
    page_title="Disease Intelligence Dashboard",
    layout="wide"
)

inject_custom_css()
require_auth()

user = get_current_user() or {}


# LOAD DATA
@st.cache_data
def load_data():

    df = pd.read_csv(
        "datasets/healthcare_surveillance_dataset.csv"
    )

    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    return df


df = load_data()


# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.title("🧠 Intelligence Filters")

country = st.sidebar.multiselect(
    "Select Country",
    options=sorted(df["Country"].unique()),
    default=["India"]
)

state = st.sidebar.multiselect(
    "Select State",
    options=sorted(df[df["Country"].isin(country)]["State"].unique()),
    default=[]
)

disease = st.sidebar.multiselect(
    "Select Disease",
    options=sorted(df["Disease"].unique()),
    default=[]
)

risk = st.sidebar.multiselect(
    "Risk Level",
    options=["Low", "Moderate", "High"],
    default=["Low", "Moderate", "High"]
)


# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df["Country"].isin(country)) &
    (df["Risk_Level"].isin(risk))
]

if state:
    filtered_df = filtered_df[
        filtered_df["State"].isin(state)
    ]

if disease:
    filtered_df = filtered_df[
        filtered_df["Disease"].isin(disease)
    ]


# =========================
# HEADER
# =========================
st.title("🌍 Disease Intelligence Dashboard")

st.caption(
    "Country-wise, state-wise, disease-based and symptom-based clinical risk analytics."
)


# =========================
# KPI CARDS
# =========================
total_cases = int(
    filtered_df["Cases"].sum()
)

avg_severity = round(
    filtered_df["Severity_Score"].mean(),
    2
)

top_disease = (
    filtered_df["Disease"]
    .value_counts()
    .idxmax()
    if not filtered_df.empty
    else "N/A"
)

high_risk_cases = int(
    filtered_df[
        filtered_df["Risk_Level"] == "High"
    ]["Cases"].sum()
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Total Cases",
        f"{total_cases:,}"
    )

with k2:
    st.metric(
        "Avg Severity",
        avg_severity
    )

with k3:
    st.metric(
        "Top Disease",
        top_disease
    )

with k4:
    st.metric(
        "High Risk Cases",
        f"{high_risk_cases:,}"
    )

st.divider()


# =========================
# COUNTRY + STATE INTELLIGENCE
# =========================
c1, c2 = st.columns([1.3, 1])

with c1:

    st.subheader("🌍 Country-wise Disease Risk")

    country_data = (
        filtered_df
        .groupby("Country")["Cases"]
        .sum()
        .reset_index()
    )

    fig_country = px.choropleth(
        country_data,
        locations="Country",
        locationmode="country names",
        color="Cases",
        color_continuous_scale="Reds",
        title="Country-wise Disease Case Density"
    )

    fig_country.update_layout(
        height=420,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(
        fig_country,
        use_container_width=True
    )

with c2:

    st.subheader("📊 State-wise Risk Ranking")

    state_data = (
        filtered_df
        .groupby("State")["Cases"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_state = px.bar(
        state_data,
        x="Cases",
        y="State",
        orientation="h",
        color="Cases",
        color_continuous_scale="Blues",
        title="Top States by Disease Cases"
    )

    fig_state.update_layout(
        height=420,
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_state,
        use_container_width=True
    )


# =========================
# DISEASE + RISK ANALYTICS
# =========================
st.divider()

d1, d2 = st.columns(2)

with d1:

    st.subheader("🦠 Disease Trend Analysis")

    disease_data = (
        filtered_df
        .groupby("Disease")["Cases"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_disease = px.bar(
        disease_data,
        x="Cases",
        y="Disease",
        orientation="h",
        color="Cases",
        color_continuous_scale="Viridis",
        title="Most Reported Diseases"
    )

    fig_disease.update_layout(
        height=420,
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_disease,
        use_container_width=True
    )

with d2:

    st.subheader("⚠️ Risk Level Distribution")

    risk_data = (
        filtered_df["Risk_Level"]
        .value_counts()
        .reset_index()
    )

    risk_data.columns = [
        "Risk Level",
        "Count"
    ]

    fig_risk = px.pie(
        risk_data,
        names="Risk Level",
        values="Count",
        hole=0.45,
        title="Clinical Risk Distribution"
    )

    fig_risk.update_layout(
        height=420
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True
    )


# =========================
# SYMPTOM INTELLIGENCE
# =========================
st.divider()

s1, s2 = st.columns(2)

with s1:

    st.subheader("🧬 Symptom Intelligence")

    symptom_series = (
        filtered_df["Symptoms"]
        .dropna()
        .str.split(", ")
        .explode()
    )

    symptom_data = (
        symptom_series
        .value_counts()
        .head(10)
        .reset_index()
    )

    symptom_data.columns = [
        "Symptom",
        "Frequency"
    ]

    fig_symptoms = px.bar(
        symptom_data,
        x="Frequency",
        y="Symptom",
        orientation="h",
        color="Frequency",
        color_continuous_scale="Teal",
        title="Most Common Symptoms"
    )

    fig_symptoms.update_layout(
        height=420,
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_symptoms,
        use_container_width=True
    )

with s2:

    st.subheader("🔥 Severity Monitoring")

    fig_severity = px.histogram(
        filtered_df,
        x="Severity_Score",
        color="Risk_Level",
        nbins=20,
        title="Severity Score Distribution"
    )

    fig_severity.update_layout(
        height=420
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True
    )


# =========================
# AI OBSERVATION
# =========================
st.divider()

st.subheader("🤖 AI Clinical Observation")

if not filtered_df.empty:

    avg_sev = round(
        filtered_df["Severity_Score"].mean(),
        2
    )

    top_symptom = (
        symptom_series
        .value_counts()
        .idxmax()
        if not symptom_series.empty
        else "N/A"
    )

    st.info(
        f"""
        **AI Observation:**  
        The selected region shows higher occurrence of **{top_disease}**.
        The average severity score is **{avg_sev}**, and the most frequent symptom is **{top_symptom}**.

        This indicates a need for continuous symptom monitoring and preventive healthcare awareness.
        """
    )

else:

    st.warning(
        "No data available for selected filters."
    )


# =========================
# RECENT RECORDS
# =========================
st.subheader("📋 Recent Disease Surveillance Records")

st.dataframe(
    filtered_df.sort_values(
        by="Date",
        ascending=False
    ).head(20),
    use_container_width=True
)


# =========================
# FOOTER
# =========================
render_footer(
    user.get("email", "")
)
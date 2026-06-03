import streamlit as st
import pandas as pd
import joblib


@st.cache_resource
def load_ml_assets():

    model = joblib.load("models/symptom_model.pkl")

    training_df = pd.read_csv("training.csv")
    master_rec = pd.read_csv("models/master_recommendations.csv")
    severity_df = pd.read_csv("Symptom-severity.csv")

    # Clean training columns
    training_df.columns = training_df.columns.str.strip()

    drop_cols = [
        "prognosis",
        "medicine",
        "Unnamed: 133"
    ]

    all_symptoms = training_df.drop(
        columns=drop_cols,
        errors="ignore"
    ).columns.tolist()

    # Clean recommendation disease names
    master_rec["Disease"] = (
        master_rec["Disease"]
        .astype(str)
        .str.strip()
    )

    # Clean severity
    severity_df["Symptom"] = (
        severity_df["Symptom"]
        .astype(str)
        .str.replace("_", " ")
        .str.lower()
        .str.strip()
    )

    sev_dict = dict(
        zip(
            severity_df["Symptom"],
            severity_df["weight"]
        )
    )

    formatted_to_tech = {
        s.replace("_", " ").title(): s
        for s in all_symptoms
    }

    return (
        model,
        master_rec,
        all_symptoms,
        sev_dict,
        formatted_to_tech
    )
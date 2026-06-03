import streamlit as st
from groq import Groq


def generate_ai_summary(
    disease,
    symptoms,
    severity,
    risk_level,
    precautions
):

    try:
        client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        prompt = f"""
        You are a healthcare AI assistant.

        Summarize this prediction in simple human language.

        Disease: {disease}
        Symptoms: {", ".join(symptoms)}
        Severity Score: {severity}
        Risk Level: {risk_level}
        Precautions: {", ".join([str(p) for p in precautions if p])}

        Include:
        1. Simple explanation
        2. What patient should do
        3. Which doctor/specialist to consult
        4. Medical disclaimer

        Keep it concise.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception:
        return "AI summary unavailable. Please consult a healthcare professional."
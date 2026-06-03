from fpdf import FPDF
from datetime import datetime


def create_pdf(
    patient_id,
    username,
    gender,
    dob,
    prediction,
    description,
    precautions,
    symptoms,
    severity,
    confidence
):

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    # =========================
    # HEADER
    # =========================
    pdf.set_fill_color(37, 99, 235)

    pdf.rect(0, 0, 210, 30, style="F")

    pdf.set_text_color(255, 255, 255)

    pdf.set_font(
        "Arial",
        "B",
        22
    )

    pdf.cell(
        0,
        18,
        "HealthAI Clinical Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    # Reset text color
    pdf.set_text_color(0, 0, 0)

    # =========================
    # PATIENT DETAILS
    # =========================
    pdf.set_font(
        "Arial",
        "B",
        15
    )

    pdf.cell(
        0,
        10,
        "Patient Information",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.set_fill_color(245, 247, 250)

    # Row 1
    pdf.cell(
        95,
        10,
        f"Patient ID: {patient_id}",
        border=1,
        fill=True
    )

    pdf.cell(
        95,
        10,
        f"Name: {username}",
        border=1,
        fill=True,
        ln=True
    )

    # Row 2
    pdf.cell(
        95,
        10,
        f"Gender: {gender}",
        border=1,
        fill=True
    )

    pdf.cell(
        95,
        10,
        f"DOB: {dob}",
        border=1,
        fill=True,
        ln=True
    )

    # Row 3
    pdf.cell(
        190,
        10,
        f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        border=1,
        fill=True,
        ln=True
    )

    pdf.ln(8)

    # =========================
    # DIAGNOSIS
    # =========================
    pdf.set_fill_color(220, 235, 255)

    pdf.set_font(
        "Arial",
        "B",
        16
    )

    pdf.cell(
        0,
        12,
        f"Primary Diagnosis: {prediction}",
        ln=True,
        fill=True
    )

    pdf.ln(5)

    # =========================
    # DESCRIPTION
    # =========================
    pdf.set_font(
        "Arial",
        "B",
        14
    )

    pdf.cell(
        0,
        10,
        "Disease Description",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.multi_cell(
        190,
        8,
        str(description)
    )

    pdf.ln(5)

    # =========================
    # SYMPTOMS
    # =========================
    pdf.set_font(
        "Arial",
        "B",
        14
    )

    pdf.cell(
        0,
        10,
        "Symptoms Selected",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.multi_cell(
        190,
        8,
        ", ".join(symptoms)
    )

    pdf.ln(5)

    # =========================
    # METRICS
    # =========================
    pdf.set_font(
        "Arial",
        "B",
        14
    )

    pdf.cell(
        0,
        10,
        "Prediction Metrics",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.set_fill_color(240, 248, 255)

    pdf.cell(
        63,
        12,
        f"Severity: {severity}",
        border=1,
        align="C",
        fill=True
    )

    pdf.cell(
        63,
        12,
        f"Confidence: {confidence}",
        border=1,
        align="C",
        fill=True
    )

    pdf.cell(
        64,
        12,
        "AI Generated",
        border=1,
        align="C",
        fill=True,
        ln=True
    )

    pdf.ln(8)

    # =========================
    # PRECAUTIONS
    # =========================
    pdf.set_font(
        "Arial",
        "B",
        14
    )

    pdf.cell(
        0,
        10,
        "Recommended Precautions",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    # Balanced precaution boxes
    for idx, item in enumerate(precautions, start=1):

        if item and str(item).strip():

            pdf.set_fill_color(248, 250, 252)

            pdf.multi_cell(
                190,
                10,
                f"{idx}. {item}",
                border=1,
                fill=True
            )

            pdf.ln(2)

    pdf.ln(6)

    # =========================
    # DISCLAIMER
    # =========================
    pdf.set_font(
        "Arial",
        "I",
        10
    )

    pdf.set_text_color(
        100,
        100,
        100
    )

    pdf.multi_cell(
        190,
        6,
        "Disclaimer: This report is AI-generated and intended for educational and preliminary healthcare guidance only. Please consult a certified healthcare professional for final medical diagnosis."
    )

    # =========================
    # RETURN PDF
    # =========================
    return bytes(
        pdf.output(dest="S")
    )
# 🏥 HealthAI Pro

## Machine Learning Based Healthcare Prediction and Recommendation System

HealthAI Pro is an AI-powered healthcare platform that predicts diseases based on user symptoms and provides personalized healthcare recommendations. The system combines Machine Learning, REST APIs, secure authentication, AI-powered chatbot assistance, voice interaction, and healthcare analytics into a unified platform.

---

## 🚀 Features

### 🔐 Authentication & Security

* User Registration and Login
* JWT Authentication
* Google OAuth Login
* Password Hashing
* Role-Based Access Control (RBAC)

### 🤖 Disease Prediction

* Symptom-Based Disease Prediction
* Random Forest & SVM Models
* Severity Index Calculation
* Confidence Score Generation
* Personalized Recommendations

### 🩺 Healthcare Assistance

* AI Healthcare Chatbot (Llama via Groq API)
* Voice-Based Interaction
* Multilingual Support
* Specialist Recommendations

### 📄 Reporting

* Professional PDF Health Reports
* Prediction History Tracking
* Clinical Insights

### 📊 Analytics Dashboard

* Disease Trend Analysis
* Symptom Intelligence
* Severity Monitoring
* Country & State Wise Healthcare Analytics

---

## 🏗️ System Architecture

User → Streamlit Frontend → Flask REST APIs → Machine Learning Models & PostgreSQL Database → Prediction & Recommendation Engine

---

## 🛠️ Technology Stack

### Frontend

* Streamlit
* Plotly
* HTML/CSS

### Backend

* Flask
* Flask-JWT-Extended
* Flask-SQLAlchemy
* REST APIs

### Database

* PostgreSQL

### Machine Learning

* Scikit-Learn
* Pandas
* NumPy

### AI Integration

* Llama Model
* Groq API

---

## 📂 Project Structure

```text
HealthAI-Pro/
│
├── backend/
├── frontend/
├── notebooks/
├── models/
├── datasets/
├── screenshots/
├── README.md
└── .gitignore
```

---

## 🧠 Machine Learning Workflow

1. Dataset Collection
2. Data Cleaning & Preprocessing
3. Feature Engineering
4. Model Training
5. Model Evaluation
6. Disease Prediction
7. Recommendation Generation

---

## 📸 Application Screenshots


### Login Page
<img width="1363" height="680" alt="Login Page" src="https://github.com/user-attachments/assets/c6923470-97d3-4429-bfd0-abc98b619e00" />

### Dashboard
<img width="1137" height="446" alt="Diseases Dashboard 2 (1)" src="https://github.com/user-attachments/assets/30a5d3c8-0300-4756-bb71-04fe7d14b38b" />

### Disease Predictor
<img width="1361" height="678" alt="Health Prediction" src="https://github.com/user-attachments/assets/11375440-4256-445a-93cb-37176ef083e8" />
<img width="1361" height="678" alt="Health Prediction" src="https://github.com/user-attachments/assets/b14a2216-3c2c-4554-85d9-6a2fbec8bb08" />

### AI Chatbot
<img width="1365" height="595" alt="AI Chatbot" src="https://github.com/user-attachments/assets/b2144ac9-1b66-457c-b920-1abb2fcacc5c" />

### PDF Report
<img width="409" height="535" alt="PDF Report" src="https://github.com/user-attachments/assets/d3208f2c-a91e-411c-8b92-49419e4e56f9" />

---

## 🔮 Future Scope

* Nearby Hospital Recommendation System
* Real-Time Clinical Data Integration
* Explainable AI (SHAP)
* Cloud Deployment
* Telemedicine Integration


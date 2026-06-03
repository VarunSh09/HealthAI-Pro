import requests


BASE_URL = "http://127.0.0.1:5000"


# SAVE PREDICTION

def save_prediction(
    token,
    payload
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.post(
        f"{BASE_URL}/save-prediction",
        json=payload,
        headers=headers
    )


# GET HISTORY

def get_prediction_history(
    token
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.get(
        f"{BASE_URL}/prediction-history",
        headers=headers
    )





# USER ANALYTICS

def get_user_analytics(token):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.get(
        f"{BASE_URL}/analytics/user",
        headers=headers
    )

def get_admin_users(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.get(
        f"{BASE_URL}/admin/users",
        headers=headers
    )



#chatbot interaction
def ask_chatbot(token, message):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.post(
        f"{BASE_URL}/chatbot",
        json={
            "message": message
        },
        headers=headers
    )




def get_weather_ai_advisory(token, latitude, longitude):
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "latitude": latitude,
        "longitude": longitude
    }

    return requests.post(
        f"{BASE_URL}/weather-ai-advisory",
        json=payload,
        headers=headers
    )
import email

from flask import Blueprint, jsonify,request
from app import db
from app.models import User
import bcrypt
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,create_refresh_token
from flask import current_app,request
from flask_jwt_extended import get_jwt
from app.email_utils import send_email
from app import oauth
from flask import url_for,redirect
from datetime import date, datetime,timedelta
import requests
from flask import redirect
from urllib.parse import urlencode
from flask import current_app
from groq import Groq

main = Blueprint("main",__name__)


def calculate_age(dob):
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

@main.route("/")
def home():
    return {"message":"Auth API Running"}


@main.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    dob = data.get("dob")
    gender = data.get("gender")

    dob_date = None
    if dob:
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            return {"error":"Invalid date format for dob. Use YYYY-MM-DD"},400
        
    # Validate required fields
    if not username or not email or not password:
        return {'error':'All fields are requiired'},400
    
    #check existing email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {'error':'Email already exists'},409
    
    hashed_password = bcrypt.hashpw( #Password hashing using bcrypt
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")
    user = User(username=username,
                email=email,
                password=hashed_password,
                role = "user",
                provider = "local",
                dob = dob,
                gender = gender 
                )
    #sending welcome email to new USERS after registration
    print("Sending test email...")
    send_email(email,username)
    print("Email sent successfully")
    
    db.session.add(user)
    db.session.commit()
    return {"message":"User registered successfully"},201

@main.route('/login',methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {"error":"Email and password required"},400
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return {'error':'Invalid credentials'},401
    
    #verify password
    password_match = bcrypt.checkpw(password.encode('utf-8'),user.password.encode('utf-8'))

    if not password_match:
        return {'error':'Invalid credentials'},401
    
    access_token = create_access_token(identity=str(user.id),additional_claims={'role':user.role})
    
    refresh_token=create_refresh_token(identity=str(user.id),additional_claims={'role':user.role})

    return {'message':'Login successful',
            'access_token':access_token,
            'refresh_token':refresh_token,
            "role":user.role
            },200
        
@main.route('/profile',methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    return{
        'id':user.id,
        'username':user.username,
        'email':user.email,
        'role': user.role,
        'dob':str(user.dob) if str(user.dob) else None,
        "age": calculate_age(user.dob) if user.dob else None,
        'gender':user.gender,
        'provider':user.provider
    },200

@main.route('/refresh',methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()

    new_access_token = create_access_token(identity=str(user_id))
    
    return {
        'access_token':new_access_token
    },200


@main.route("/logout",methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()['jti']

    current_app.blacklist.add(jti)

    return {
        "message":"Logout out successfully"
    },200

@main.route("/admin/users",methods = ["GET"])
@jwt_required()
def get_all_users():
    claims = get_jwt()

    if claims["role"]!='admin':
        return {"error":"Admin access required"},403
    
    users = User.query.all()

    data = []
    for user in users:
        data.append({
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'role':user.role
        })
    return {'users':data},200


@main.route("/welcome-email",methods=["GET"])

def send_mail():
    print("Sending test email...")
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    send_email(
        f"{email}",
        username
    )
    print("Email sent successfully")
    return {"message": "Email sent"},200

@main.route("/google/login")
def google_login():
    redirect_uri = url_for("main.google_callback",_external=True)

    return oauth.google.authorize_redirect(redirect_uri, prompt="select_account")

@main.route("/google/callback")
def google_callback():
    token = oauth.google.authorize_access_token()

    user_info = token["userinfo"]
    access_token_google = token['access_token']

    headers = {"Authorization":f"Bearer {access_token_google}"}
     
    print("Calling People API...")

    people_response = requests.get(
        "https://people.googleapis.com/v1/people/me" "?personFields=genders,birthdays",
        headers = headers,timeout=15
    )
    print("People APi....")
 
    people_data = people_response.json()
         
    gender = None
    dob = None
    
     

    if "genders" in people_data:
        gender = people_data["genders"][0].get("value")

    if "birthdays" in people_data:
        birthday = people_data["birthdays"][0]["date"]

        year = birthday.get("year",2000)
        month = birthday.get("month",1)
        day = birthday.get("day",1)

        dob = date(year,month,day)

    email = user_info["email"]
    username = user_info["name"]
    
    user = User.query.filter_by(email = email).first()

    if not user:
        user = User(
            username = username,
            email = email,
            password = None,
            role = "user",
            provider= "google",
            gender = gender,
            dob = dob
        )
        db.session.add(user)
        db.session.commit()
        #sending welcome email to new USERS after registration
        print("Sending test email...")
        send_email(email,username)
        print("Email sent successfully")

    access_token = create_access_token(identity=str(user.id),additional_claims={"role":user.role})

    refresh_token = create_refresh_token(identity=str(user.id),additional_claims={"role":user.role})
    
    # return {
    #     "message":"Google login successful",
    #     "access_token":access_token,
    #     "refresh_token":refresh_token,
    #     "role":user.role,
    #     "provider":user.provider,
    #     "gender":user.gender,
    #     "dob":str(user.dob) if user.dob else None
    #               },200
    params = urlencode({
    "token": access_token
})

    return redirect(
    f"http://localhost:8501/?{params}"
)



# =========================
# SAVE PREDICTION
# =========================

@main.route("/save-prediction",methods=["POST"])
@jwt_required()
def save_prediction():

    try:
        current_user = get_jwt_identity() 
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE id = %s",
            (current_user,)
        )
        user_row = cursor.fetchone()
        if not user_row:

            return jsonify({
                "error": "User not found"
            }), 404

        user_id = user_row[0]
        data = request.get_json()
        query = """
        INSERT INTO patient_records
        (
            user_id,
            symptoms,
            predicted_disease,
            confidence_score,
            severity_score
        )
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            data.get("symptoms"),
            data.get("predicted_disease"),
            data.get("confidence_score"),
            data.get("severity_score")
        )

        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Prediction saved"
        }), 201

    except Exception as e:

        import traceback

        traceback.print_exc()

        print("ERROR:", str(e))

        return jsonify({
        "error": str(e)
        }), 500



# =========================
# GET PREDICTION HISTORY
# =========================

@main.route(
    "/prediction-history",
    methods=["GET"]
)
@jwt_required()
def prediction_history():

    try:

        # JWT returns email
        current_user = get_jwt_identity()

        conn = db.engine.raw_connection()

        cursor = conn.cursor()


        # Get actual user id
        cursor.execute(
            "SELECT id FROM users WHERE id = %s",
            (current_user,)
        )

        user_row = cursor.fetchone()

        if not user_row:

            return jsonify([]), 200

        user_id = user_row[0]

        query = """
        SELECT
            record_id,
            symptoms,
            predicted_disease,
            confidence_score,
            severity_score,
            prediction_date
        FROM patient_records
        WHERE user_id = %s
        ORDER BY prediction_date DESC
        """

        cursor.execute(
            query,
            (user_id,)
        )

        rows = cursor.fetchall()

        columns = [
            "record_id",
            "symptoms",
            "predicted_disease",
            "confidence_score",
            "severity_score",
            "prediction_date"
        ]

        result = []

        for row in rows:

            result.append(
                dict(zip(columns, row))
            )

        cursor.close()
        conn.close()
        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    



# USER ANALYTICS

@main.route(
    "/analytics/user",
    methods=["GET"]
)
@jwt_required()
def user_analytics():

    try:

        current_user = get_jwt_identity()

        conn = db.engine.raw_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            predicted_disease,
            confidence_score,
            severity_score,
            prediction_date
        FROM patient_records
        WHERE user_id = %s
        ORDER BY prediction_date DESC
        """

        cursor.execute(
            query,
            (current_user,)
        )

        rows = cursor.fetchall()

        result = []

        for row in rows:

            result.append({
                "disease": row[0],
                "confidence": float(row[1]),
                "severity": float(row[2]),
                "date": str(row[3])
            })

        cursor.close()
        conn.close()
        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    


#ChatBot Route
@main.route("/chatbot", methods=["POST"])
@jwt_required()
def chatbot():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return {"error": "Message is required"}, 400

    try:
        client = Groq(api_key=current_app.config["GROQ_API_KEY"])
        
        system_prompt = f"""
You are HealthAI Pro, an AI-powered healthcare assistant integrated into the
Machine Learning Based Healthcare Prediction and Recommendation System.

User Information:
- Name: {user.username}
- Gender: {user.gender}
- Date of Birth: {user.dob}

Your Responsibilities:
- Provide safe and helpful healthcare guidance
- Explain diseases and symptoms in simple language
- Suggest suitable doctor specialists when necessary
- Recommend precautions and healthy lifestyle habits
- Support multilingual healthcare conversations
- Maintain a professional and empathetic tone

Important Rules:
- Only answer healthcare and medical-related questions
- Ignore or politely refuse any out-of-context questions
- If the user asks about coding, politics, movies, hacking,
  mathematics, general knowledge, or non-medical topics,
  politely say:
  "I am a healthcare assistant and can only answer medical or health-related questions."

Safety Rules:
- Never claim to be a real doctor
- Never provide dangerous medical advice
- Never prescribe exact medicines or dosages
- Always recommend consulting a certified healthcare professional
- Clearly mention that responses are AI-generated healthcare guidance

Emergency Handling:
If the user mentions symptoms such as:
- chest pain
- breathing difficulty
- severe bleeding
- unconsciousness
- stroke symptoms
- suicidal thoughts

Immediately advise emergency medical attention.

Response Style:
- Keep answers short, clear, and precise
- Avoid long paragraphs
- Use bullet points when necessary
- Keep responses easy to understand
- Stay strictly within healthcare context
"""
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        response = completion.choices[0].message.content

        return {
            "response": response
        }, 200

    except Exception as e:
        return {
            "error": str(e)
        }, 500
    



@main.route("/weather-ai-advisory", methods=["POST"])
@jwt_required()
def weather_ai_advisory():

    try:
        data = request.get_json()

        lat = data.get("latitude")
        lon = data.get("longitude")

        if not lat or not lon:
            return jsonify({
                "error": "Location required"
            }), 400

        # =========================
        # WEATHER API
        # =========================
        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}"
            f"&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m"
        )

        weather_res = requests.get(weather_url, timeout=5)

        current = weather_res.json().get("current", {})

        temperature = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")

        # =========================
        # REVERSE GEOCODING
        # =========================
        geo_url = (
    "https://nominatim.openstreetmap.org/reverse"
    f"?lat={lat}&lon={lon}&format=json"
)

        geo_res = requests.get(geo_url,headers={
        "User-Agent": "HealthAIPro/1.0"},timeout=5)

        location_name = "Unknown City"
        state_name = "Unknown State"
        country = "Unknown Country"
        if geo_res.status_code == 200:

            geo_data = geo_res.json()

            address = geo_data.get("address", {})

            location_name = (
    address.get("city")
    or address.get("town")
    or address.get("village")
    or "Unknown City"
)

            state_name = (
    address.get("state")
    or address.get("region")
    or "Unknown State"
)

            country = address.get(
                "country",
                "Unknown Country"
            )
        else:
            print("Reverse geocoding failed:", geo_res.text)
        # =========================
        # GROQ AI
        # =========================
        client = Groq(
            api_key=current_app.config.get(
                "GROQ_API_KEY"
            )
        )

        prompt = f"""
        You are an AI healthcare weather advisory assistant.

        Location: {location_name}, {country}

        Weather:
        Temperature: {temperature}°C
        Humidity: {humidity}%

        Generate:
        1. Short health warning
        2. Two preventive recommendations
        3. Risk level

        Keep response concise and professional.
        """

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        ai_text = completion.choices[0].message.content

        return jsonify({

    "location": location_name,
    "state": state_name,
    "country": country,

    "latitude": lat,
    "longitude": lon,

    "temperature": temperature,
    "humidity": humidity,

    "ai_advisory": ai_text

}), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
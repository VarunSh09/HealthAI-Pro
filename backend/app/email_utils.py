import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_email(to_email, username):

    message = Mail(
        from_email='varunsharma123156@gmail.com',
        to_emails=to_email,
        subject="Welcome to HEALTHPRO AI",
        html_content=f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background:#f4f7fb; padding:20px;">
    <div style="
        max-width:600px;
        margin:auto;
        background:white;
        border-radius:10px;
        padding:30px;
        box-shadow:0 2px 10px rgba(0,0,0,0.1);
    ">
        <h1 style="color:#1E88E5; text-align:center;">
            HEALTHPRO AI
        </h1>
        <h2>Hello, {username}! 👋</h2>
        <p>
            Welcome to <strong>HEALTHPRO AI</strong>.
            We are excited to have you onboard.
        </p>
        <p>
            Our platform provides AI-powered healthcare predictions
            and personalized recommendations based on your symptoms.
        </p>
        <p>
            Thank you for joining us.
        </p>
        <hr>
        <p style="font-size:12px; color:gray; text-align:center;">
            © 2026 HEALTHPRO AI
        </p>
    </div>
</body>
</html>
"""
    )
        
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response
    except Exception as e:
        print(f"Error sending email: {e}")
        return None
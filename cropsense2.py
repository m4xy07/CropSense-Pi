import smtplib
from email.mime.text import MIMEText
from secret import SECRET_TWILIO_ACCOUNT_SID, SECRET_TWILIO_AUTH_TOKEN, SECRET_TWILIO_PHONE_NUMBER, SECRET_RECIPIENT_PHONE_NUMBER

HIGH_TEMP_THRESHOLD = 35.0
HIGH_SOIL_MOISTURE_THRESHOLD = 80.0
HIGH_AQI_THRESHOLD = 1000

def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "your_email@example.com"
    msg["To"] = "recipient_email@example.com"

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("your_email@example.com", "your_password")
        server.sendmail("your_email@example.com", "recipient_email@example.com", msg.as_string())

def check_alerts(temperature, soil_moisture, air_quality_index):
    if temperature > HIGH_TEMP_THRESHOLD:
        send_email_alert("High Temperature Alert", f"Temperature has exceeded {HIGH_TEMP_THRESHOLD}C")

    if soil_moisture > HIGH_SOIL_MOISTURE_THRESHOLD:
        send_email_alert("High Soil Moisture Alert", f"Soil moisture has exceeded {HIGH_SOIL_MOISTURE_THRESHOLD}%")

    if air_quality_index > HIGH_AQI_THRESHOLD:
        send_email_alert("High AQI Alert", f"Air Quality Index has exceeded {HIGH_AQI_THRESHOLD}")

import os
import smtplib
import requests
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

url = "https://ita-pak.blsinternational.com/Global/account/login"

# Fetch email credentials from environment variables
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
email_password = os.environ.get("EMAIL_PASSWORD")

def send_email_alert():
    subject = "Visa Portal is Now Active!"
    body = f"The visa appointment portal is now accessible: {url}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, email_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

def check_site():
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

while True:
    if check_site():
        send_email_alert()
        print("Website available — email sent!")
        break
    else:
        print("Website not available. Retrying in 2 minutes.")
    time.sleep(120)  # Wait for 2 minutes

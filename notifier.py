import requests
from dotenv import load_dotenv
import os

load_dotenv()

error_message = "There is something wrong with the site. Please check it as soon as possible."

def send_notification(message):
    url = f"https://api.telegram.org/bot{os.getenv('TG_TOKEN')}/sendMessage"

    params = {
        "chat_id": os.getenv('TG_CHAT_ID'),
        "text": f"🚨 ALERT: {message}"
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        print("Notification sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification: {e}")
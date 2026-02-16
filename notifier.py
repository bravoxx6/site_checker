import requests

API_TOKEN = '8189707273:AAFCh07X6Ydkr7SZhP3hAg9qqji5SjlSZpw'
chat_id = 881438885

error_message = "The site is down"

def send_notification(message):
    url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"

    params = {
        "chat_id": chat_id,
        "text": f"🚨 ALERT: {message}"
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        print("Notification sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification: {e}")
# telegram_util.py
import requests
import os

def send_telegram(message):
    token = os.getenv("7594519988:AAGGDZ0WgpLZ_3ArIWy8SPKrTwwCuFUWMGs")
    chat_id = os.getenv("-1002652468152")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

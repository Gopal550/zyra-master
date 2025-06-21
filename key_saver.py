import os
import json
import re
from datetime import datetime
import requests

INSTANCE_ID = "instance126727"
TOKEN = "2nmo6sl5l4ry94le"
ADMIN_NUMBER = "918600609295"
SAVE_FOLDER = "API keys Json"

patterns = {
    "OPENAI": r"sk-[a-zA-Z0-9\-]+",
    "RAZORPAY": r"rzp_(test|live)_[a-zA-Z0-9]+",
    "STRIPE": r"pk_(test|live)_[a-zA-Z0-9]+",
    "GITHUB": r"ghp_[a-zA-Z0-9]+",
    "SENDGRID": r"SG\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",
    "JWT": r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"
}

def identify_service(key):
    for service, pattern in patterns.items():
        if re.fullmatch(pattern, key):
            return service
    return None

def send_whatsapp_message(number, body):
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    data = {"token": TOKEN, "to": number, "body": body}
    try:
        requests.post(url, data=data)
    except:
        pass

def save_key_auto(msg):
    key = msg.strip()
    service = identify_service(key)

    if not service:
        send_whatsapp_message(ADMIN_NUMBER, "❌ Yeh valid API key nahi hai. Kripya sahi key bhejo.")
        return {"error": "invalid key"}

    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    filename = os.path.join(SAVE_FOLDER, f"{service.lower()}.json")
    data = {
        "value": key,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    send_whatsapp_message(ADMIN_NUMBER, f"✅ {service} API key save ho gayi hai.")
    return {"status": "saved", "service": service}

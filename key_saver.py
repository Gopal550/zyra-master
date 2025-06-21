import os
import json
import re
from datetime import datetime
import requests

INSTANCE_ID = "instance126727"
TOKEN = "2nmo6sl5l4ry94le"
ADMIN_NUMBER = "918600609295"
SAVE_FOLDER = "API keys Json"

# Updated patterns to detect keys
patterns = {
    "OPENAI": r"sk-[a-zA-Z0-9\-]{20,}",
    "RAZORPAY": r"rzp_(test|live)_[a-zA-Z0-9]+",
    "STRIPE": r"pk_(test|live)_[a-zA-Z0-9]+",
    "GITHUB": r"ghp_[a-zA-Z0-9]+",
    "SENDGRID": r"SG\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",
    "JWT": r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"
}

# Identify service based on pattern
def identify_service(key):
    for service, pattern in patterns.items():
        if re.fullmatch(pattern, key):
            print(f"✅ Match found: {service}")
            return service
    print("❌ No matching service found for key:", key)
    return None

# Send WhatsApp reply
def send_whatsapp_message(number, body):
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    data = {"token": TOKEN, "to": number, "body": body}
    try:
        res = requests.post(url, data=data)
        print("📤 WhatsApp sent:", res.text)
    except Exception as e:
        print("❌ WhatsApp send error:", e)

# Main saving logic
def save_key_auto(msg):
    print("📩 Received message:", msg)
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
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ API key saved in {filename}")
        send_whatsapp_message(ADMIN_NUMBER, f"✅ {service} API key save ho gayi hai.")
        return {"status": "saved", "service": service}
    except Exception as e:
        print("❌ Error saving key:", e)
        send_whatsapp_message(ADMIN_NUMBER, "❌ Key save karne me error aaya.")
        return {"error": str(e)}

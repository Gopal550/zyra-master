import os
import json
from datetime import datetime

API_KEY_FILE = "data/api_keys.json"

def detect_service_from_key(key):
    if key.startswith("sk-"):
        return "OPENAI"
    elif key.startswith("rzp_test_") or key.startswith("rzp_live_"):
        return "RAZORPAY"
    elif key.startswith("pk_live_") or key.startswith("pk_test_"):
        return "STRIPE"
    elif key.startswith("SG."):
        return "SENDGRID"
    elif key.startswith("ghp_"):
        return "GITHUB"
    elif "token" in key.lower():
        return "TOKEN"
    elif "secret" in key.lower():
        return "SECRET"
    else:
        return None

def detect_and_save_key(key):
    service = detect_service_from_key(key)
    if not service:
        return {"status": "error", "error": "Invalid API key format"}

    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            keys = json.load(f)
    else:
        keys = {}

    keys[service] = {
        "value": key,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(API_KEY_FILE, "w") as f:
        json.dump(keys, f, indent=2)

    return {"status": "success", "service": service}

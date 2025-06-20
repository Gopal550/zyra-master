import os
import json
import re
from datetime import datetime

KEY_STORE = "api_keys.json"

# Pattern-based detection of API keys
def detect_service_and_type(key):
    patterns = {
        "OPENAI": r"sk-[a-zA-Z0-9]{32,}",
        "RAZORPAY": r"rzp_(test|live)_[a-zA-Z0-9]+",
        "STRIPE": r"pk_(test|live)_[a-zA-Z0-9]+",
        "GITHUB": r"ghp_[a-zA-Z0-9]+",
        "FIREBASE": r"AAAA[a-zA-Z0-9_-]{7}:[a-zA-Z0-9_-]{140}",
        "TWILIO": r"SK[0-9a-fA-F]{32}",
        "VERCEL": r"vercel_[a-zA-Z0-9_]+",
        "SUPABASE": r"supabase_[a-zA-Z0-9]+",
        "MAPBOX": r"pk\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+"
    }

    for service, pattern in patterns.items():
        if re.fullmatch(pattern, key):
            return service, "API_KEY"
    return None, None

def load_keys():
    if not os.path.exists(KEY_STORE):
        return {}
    with open(KEY_STORE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(KEY_STORE, "w") as f:
        json.dump(keys, f, indent=2)

def save_key_auto(msg):
    key = msg.strip()
    service, key_type = detect_service_and_type(key)

    if not service:
        print("❌ Invalid or unknown API key format!")
        return {"error": "Invalid key format or unknown service."}

    keys = load_keys()

    keys[service] = {
        "value": key,
        "type": key_type,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    save_keys(keys)
    print(f"✅ Saved {service} key successfully!")
    return {"status": "saved", "service": service}

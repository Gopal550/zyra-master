from flask import Flask, request, jsonify
import os, json, time, threading, requests
from api_key_auto_scanner import check_keys_and_notify
from zyra_key_manager import start_monitoring
from key_saver import save_key_auto

app = Flask(__name__)

# WhatsApp message sender
def send_whatsapp_message(number, message):
    instance_id = "instance126727"
    token = "2nmo6sl5l4ry94le"
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = {"token": token, "to": number, "body": message}
    try:
        res = requests.post(url, data=payload)
        return res.json()
    except Exception as e:
        print("Error sending WhatsApp message:", e)

# Scan active services
def get_active_services():
    files = []
    for filename in os.listdir("data"):
        if filename.endswith(".json") and "message_sent" not in filename:
            name = filename.replace(".json", "")
            if name.lower() not in ["etc", "test", "dummy"]:
                files.append(name)
    return files

# Check missing keys & alert
def check_keys_and_notify():
    files = get_active_services()
    sent_flag_file = "data/message_sent.json"
    number = "918600609295"

    if os.path.exists(sent_flag_file):
        with open(sent_flag_file) as f:
            sent_flags = json.load(f)
    else:
        sent_flags = {}

    path = 'data/api_keys.json'
    key_found = False
    api_data = {}

    if os.path.exists(path):
        with open(path) as f:
            api_data = json.load(f)

    for name in files:
        key_found = name in api_data and api_data[name].get("value")
        if not key_found and not sent_flags.get(name):
            send_whatsapp_message(number, f"Zyra: Mujhe {name.upper()} API key chahiye, please bhejo.")
            sent_flags[name] = True
        elif key_found and not sent_flags.get(name + "_done"):
            send_whatsapp_message(number, f"Zyra: Mujhe {name.upper()} API key lag gayi hai ✅")
            sent_flags[name + "_done"] = True

    with open(sent_flag_file, "w") as f:
        json.dump(sent_flags, f)

# Background thread to check every 10 minutes
def run_checker():
    while True:
        check_keys_and_notify()
        time.sleep(600)

# Load Zyra data
def load_data():
    files = get_active_services()
    data = {}
    for name in files:
        path = f'data/{name}.json'
        if os.path.exists(path):
            with open(path) as f:
                data[name] = json.load(f)
        else:
            data[name] = {}
    return data

zyra_data = load_data()

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

@app.route("/receive_key", methods=["POST"])
def receive_key():
    data = request.json
    msg = data.get("body", "").replace("\n", "").strip()

    try:
        result = save_key_auto(msg)
        if "error" in result:
            return {"error": result["error"]}, 400
        return {"status": "received"}, 200
    except Exception as e:
        print("❌ Error in receive_key:", e)
        return {"error": "Something went wrong while saving key."}, 500

# Start background thread + server
if __name__ == "__main__":
    threading.Thread(target=run_checker, daemon=True).start()
    start_monitoring()
    app.run(host="0.0.0.0", port=10000)

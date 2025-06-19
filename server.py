
from flask import Flask, jsonify
import json, os, requests

app = Flask(__name__)

instance_id = "instance126727"
token = "2nmo6sl5l4ry94le"
admin_number = "+918600609295"

def load_data():
    files = ["brand", "affiliate", "live_video", "strategy", "api_keys", "interaction_and_learning_logic"]
    data = {}
    for name in files:
        path = f"data/{name}.json"
        if os.path.exists(path):
            with open(path) as f:
                data[name] = json.load(f)
        else:
            data[name] = {}
    return data

def send_whatsapp_message(number, message):
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = {
        "token": token,
        "to": number,
        "body": message
    }
    requests.post(url, data=payload)

def check_and_alert():
    zyra_data = load_data()
    keys = zyra_data.get("api_keys", {})
    sent_flag_file = "data/message_sent.json"

    if not keys:
        if not os.path.exists(sent_flag_file):
            send_whatsapp_message(admin_number, "Zyra: Mujhe API keys chahiye, please bhejo 🙏")
            with open(sent_flag_file, "w") as f:
                json.dump({"sent": True}, f)
    else:
        if os.path.exists(sent_flag_file):
            os.remove(sent_flag_file)

zyra_data = load_data()
check_and_alert()

@app.route("/")
def home():
    return {
        "status": "Zyra is active",
        "note": "Auto-check running for API keys",
        "files_loaded": list(zyra_data.keys())
    }

@app.route("/status")
def status():
    return jsonify(zyra_data)

if __name__ == "__main__":
    app.run(debug=True)


def load_data():
    files = ["brand", "affiliate", "live_video", "strategy", "api_keys", "interaction_and_learning_logic"]
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

#  This is the corrected line for Render public server:
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, jsonify
import json, os

import requests

def send_whatsapp_message(number, message):
    instance_id = "instance126727"
    token = "2nmo6sl5l4ry94le"

    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = {
        "token": token,
        "to": number,
        "body": message
    }

    res = requests.post(url, data=payload)
    return res.json()
    
    if not zyra_data.get("api_keys"):
        
    send_whatsapp_message("+918600609295", "Zyra: Mujhe API key chahiye please bhejo 🧠")
app = Flask(__name__)

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

# ✅ This is the corrected line for Render public server:
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

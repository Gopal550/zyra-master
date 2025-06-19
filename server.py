from flask import Flask, request, jsonify
import os, json, requests

app = Flask(__name__)

# WhatsApp Details
instance_id = "instance126727"
token = "2nmo6sl5l4ry94le"
admin_number = "+918600609295"

# Paths
api_file = "data/api_keys.json"
sent_flag_file = "data/message_sent.json"

def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def send_whatsapp(number, message):
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = {"token": token, "to": number, "body": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Message send error:", e)

def format_label(key_name):
    return key_name.upper().replace("_", " ") + " API key"

def check_keys_and_notify():
    api_keys = load_json(api_file)
    sent_flags = load_json(sent_flag_file)
    updated = False

    for key in api_keys:
        value = api_keys.get(key, "")
        sent = sent_flags.get(key, "")

        if value and sent != "received":
            send_whatsapp(admin_number, f"{format_label(key)} mil gai hai ✅")
            sent_flags[key] = "received"
            updated = True
        elif not value and sent != "requested":
            send_whatsapp(admin_number, f"Mujhe {format_label(key)} chahiye, please bhejo.")
            sent_flags[key] = "requested"
            updated = True

    if updated:
        save_json(sent_flag_file, sent_flags)

@app.route("/")
def home():
    return {"status": "Zyra is active", "message": "API key smart automation running"}

@app.route("/receive_key", methods=["POST"])
def receive_key():
    data = request.get_json()
    key_type = data.get("type")
    key_value = data.get("value")

    if not key_type or not key_value:
        return jsonify({"error": "Missing type or value"}), 400

    api_keys = load_json(api_file)
    sent_flags = load_json(sent_flag_file)

    api_keys[key_type] = key_value
    sent_flags[key_type] = "received"

    save_json(api_file, api_keys)
    save_json(sent_flag_file, sent_flags)

    send_whatsapp(admin_number, f"{format_label(key_type)} lag gai hai ✅")
    return jsonify({"message": "API key saved successfully"}), 200

if __name__ == "__main__":
    check_keys_and_notify()
    app.run()


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

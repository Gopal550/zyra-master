from flask import Flask, request
from zyra_key_manager import detect_and_save_key
import requests

app = Flask(__name__)

# WhatsApp message bhejne ka function
def send_whatsapp_message(number, message):
    instance_id = "instance126727"
    token = "2nmo6sl5l4ry94le"
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = {"token": token, "to": number, "body": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("WhatsApp send error:", e)

# WhatsApp se API key receive karne wala route
@app.route("/receive_key", methods=["POST"])
def receive_key():
    data = request.json
    msg = data.get("body", "").replace("\n", "").strip()
    sender = data.get("to", "918600609295")

    try:
        result = detect_and_save_key(msg)
        if result["status"] == "error":
            send_whatsapp_message(sender, f"❌ {result['error']}")
            return {"error": result["error"]}, 400

        send_whatsapp_message(sender, f"✅ {result['service']} API key save ho gayi hai.")
        return {"status": "saved", "service": result["service"]}, 200
    except Exception as e:
        print("❌ Error in receive_key:", e)
        send_whatsapp_message(sender, "❌ Internal server error while saving key.")
        return {"error": "server error"}, 500

# Flask app run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, jsonify
import json, os

app = Flask(__name__)

def load_data():
    files = ["brand", "affiliate", "live_video", "strategy", "api_keys"]
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

if __name__ == "__main__":
    app.run(debug=True)

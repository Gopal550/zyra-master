import os, re, json, requests
from datetime import datetime, timedelta

WHATSAPP_NUMBER = "918600609295"
INSTANCE_ID = "instance126727"
TOKEN = "2nmo6sl5l4ry94le"
KEY_STORE = "data/api_keys.json"

def send_whatsapp_message(msg):
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    payload = {"token": TOKEN, "to": WHATSAPP_NUMBER, "body": msg}
    try: requests.post(url, data=payload)
    except: pass

def load_keys():
    if not os.path.exists(KEY_STORE): return {}
    with open(KEY_STORE, "r") as f: return json.load(f)

def save_key(name, value):
    keys = load_keys()
    keys[name] = {"value": value, "date": datetime.now().strftime("%Y-%m-%d")}
    with open(KEY_STORE, "w") as f: json.dump(keys, f, indent=2)

def get_expiring_keys():
    keys = load_keys()
    expiring = []
    now = datetime.now()
    for name, info in keys.items():
        try:
            added = datetime.strptime(info.get("date", ""), "%Y-%m-%d")
            if 5 <= (now - added).days <= 7:
                expiring.append(name)
        except: continue
    return expiring

def scan_code(folder="."):
    patterns = ["key", "token", "secret", "client"]
    found = set()
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if any(p in line.lower() for p in patterns):
                            match = re.search(r'(api_key|access_token|secret|client_id|token)[\s:=]+["\']?([\w\-]{8,})', line, re.I)
                            if match:
                                found.add(match.group(1))
    return found

def check_and_alert():
    found_keys = scan_code()
    saved_keys = load_keys()
    for key in found_keys:
        if key not in saved_keys:
            send_whatsapp_message(f"Zyra: Mujhe {key.upper()} API key chahiye, please bhejo.")

    for key in get_expiring_keys():
        send_whatsapp_message(f"Zyra: {key.upper()} API key 1-2 din me expire hone wali hai, please update karo.")

if __name__ == "__main__":
    check_and_alert()

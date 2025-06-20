import os, re, json, requests, datetime

WHATSAPP_NUMBER = "918600609295" INSTANCE_ID = "instance126727" TOKEN = "2nmo6sl5l4ry94le" KEY_STORE = "data/api_keys.json"

=== Send WhatsApp Message ===

def send_whatsapp_message(number, message): url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat" data = {"token": TOKEN, "to": number, "body": message} try: res = requests.post(url, data=data) print("✅ Message sent:", res.json()) except Exception as e: print("❌ Error sending message:", e)

=== Load Saved Keys ===

def load_keys(): if not os.path.exists(KEY_STORE): return {} try: with open(KEY_STORE, "r") as f: return json.load(f) except: return {}

=== Save or Update Key ===

def save_key(name, value): keys = load_keys() keys[name] = {"value": value, "date": datetime.datetime.now().isoformat()} os.makedirs(os.path.dirname(KEY_STORE), exist_ok=True) with open(KEY_STORE, "w") as f: json.dump(keys, f)

=== Check for Expiring Keys ===

def get_expiring_keys(): keys = load_keys() expiring = [] now = datetime.datetime.now() for name, info in keys.items(): try: set_time = datetime.datetime.fromisoformat(info.get("date")) days_passed = (now - set_time).days if days_passed >= 5:  # 7-day cycle, alert at day 5-6 expiring.append(name) except: continue return expiring

=== Scan Code for API Key Usage ===

def scan_code(folder="."): patterns = ["key", "token", "secret", "client"] found = set() for root, _, files in os.walk(folder): for file in files: if file.endswith(".py"): path = os.path.join(root, file) try: with open(path, "r", encoding="utf-8", errors="ignore") as f: for line in f: for word in line.split(): if any(p in word.lower() for p in patterns): match = re.search(r'(api_key|access_token|secret|client_id|token)[\s:=]+["\']?([\w\-]{8,})', line, re.I) if match: found.add(match.group(1)) except: continue return found

=== Main Scanner Function ===

def run_api_key_scanner(): needed = scan_code() saved = load_keys() expiring = get_expiring_keys() for key in needed: if key not in saved or key in expiring: send_whatsapp_message(WHATSAPP_NUMBER, f"Zyra: Mujhe {key.upper()} API key chahiye, please bhejo.")


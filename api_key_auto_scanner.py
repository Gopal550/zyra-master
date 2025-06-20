
def check_keys_and_notify():
    import re
    files = os.listdir('data')
    sent_flag_file = "data/message_sent.json"
    number = "918600609295"

    # Already sent messages
    if os.path.exists(sent_flag_file):
        with open(sent_flag_file) as f:
            sent_flags = json.load(f)
    else:
        sent_flags = {}

    for file in files:
        if not file.endswith('.json'):
            continue

        path = os.path.join('data', file)
        with open(path) as f:
            data = json.load(f)

        for key, value in data.items():
            print(f"🛠 Checking: {file} - {key} = {value}")
            match = re.search(r"(api|access|client|secret|bearer|token)", key.lower())
            if match:
                key_type = extract_key_type(key)
                name = file.replace(".json", "").upper()
                flag_key = f"{name}_{key_type}"

                if not value.get("value") and not sent_flags.get(flag_key):
                    message = f"Zyra: Mujhe {name} {key_type} API key chahiye, please bhejo."
                    print(f"📲 Sending message for: {name} - {key_type}")
                    send_whatsapp_message(number, message)
                    sent_flags[flag_key] = True

    with open(sent_flag_file, "w") as f:
        json.dump(sent_flags, f)

def run_api_key_scanner():
    try:
        check_keys_and_notify()
    except Exception as e:
        print("Scanner crashed:", e)

def extract_key_type(key_name):
    key_types = ["api", "access", "client", "secret", "bearer", "token", "key"]
    for kt in key_types:
        if kt in key_name.lower():
            return kt.upper()
    return "UNKNOWN"

import json
import os

def save_key(service_name, key_value):
    file_path = "data/api_keys.json"

    # Load existing keys
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            keys = json.load(f)
    else:
        keys = {}

    # Save the key
    keys[service_name.lower()] = key_value.strip()

    # Write back to file
    with open(file_path, "w") as f:
        json.dump(keys, f, indent=2)
    print(f"✅ Saved key for {service_name}")

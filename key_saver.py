from zyra_key_manager import detect_and_save_key

def save_key_auto(msg):
    try:
        return detect_and_save_key(msg)
    except Exception as e:
        print("❌ Error in save_key_auto:", e)
        return {"status": "error", "error": str(e)}

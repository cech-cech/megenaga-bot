import os
import requests
import time

TOKEN = os.environ.get("BOT_TOKEN")

# Delete Webhook first
requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
print("Webhook deleted. Starting Telegram listener on Render...")

offset = 0
while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=10"
        res = requests.get(url).json()
        
        for update in res.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "")
            
            print(f"Received message: '{text}' from {chat_id}")
            
            if chat_id:
                reply = "📦 እንኳን ወደ መገናኛ ሎጅስቲክስ ቦት በሰላም መጡ!\n\n1. 🚛 ተሽከርካሪ ለመመዝገብ\n2. 📦 እቃ ለመመዝገብ"
                send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                payload = {"chat_id": chat_id, "text": reply}
                requests.post(send_url, json=payload)
                print(f"Successfully replied to {chat_id}!")
                
    except Exception as e:
        print(f"Error: {e}")
        
    time.sleep(1)

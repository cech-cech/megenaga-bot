import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot

# Simple dummy server to keep Render Web Service happy with an open port
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Megenaga Bot is Running!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Start dummy server in background thread
threading.Thread(target=run_dummy_server, daemon=True).start()

# Telegram Bot Setup
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

try:
    bot.remove_webhook()
    print("Webhook deleted successfully.")
except Exception as e:
    print(f"Error removing webhook: {e}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "እንኳን ወደ መገናኛ ቦት በደህና መጡ! / Welcome to Megenaga Bot!")

print("Starting Telegram listener on Render...")
bot.infinity_polling(skip_pending=True)

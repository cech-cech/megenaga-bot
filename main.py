import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import telebot

# Get Token from Render Environment Variables or direct string backup
TOKEN = os.environ.get('BOT_TOKEN', '8973955022:AAEqz4VvLwDWnBUX2jy7BDrHOk9PlZ7Ef_k')
bot = telebot.TeleBot(TOKEN)

# Simple HTTP Server for Render Port Binding
def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"HTTP Dummy Server running on port {port}")
    httpd.serve_forever()

# Handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "እንኳን ወደ መገናኛ ቦት በደህና መጡ! / Welcome to Megenaga Bot!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"የላኩልን መልዕክት ደርሶናል: {message.text}")

if __name__ == '__main__':
    # Start HTTP Server in background thread for Render
    threading.Thread(target=run_http_server, daemon=True).start()
    
    # Run Telegram Bot Long Polling
    print("Telegram Bot is starting...")
    bot.infinity_polling(skip_pending=True)

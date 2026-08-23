import os
from flask import Flask, request
import telebot

TOKEN = os.environ.get('BOT_TOKEN', '8237883909:AAErjE-UpZeZzjdMhISD6lFAoVSf7KaHQrs')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Telegram Message Handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "እንኳን ወደ መገናኛ ቦት በደህና መጡ! / Welcome to Megenaga Bot!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"የላኩልን መልዕክት ደርሶናል: {message.text}")

# Webhook Endpoint for Render
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # Set webhook to Render primary URL
    render_url = f"https://megenaga-logistics-bot.onrender.com/{TOKEN}"
    bot.set_webhook(url=render_url)
    return "Bot Webhook Activated Successfully!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

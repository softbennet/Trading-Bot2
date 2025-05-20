from telegram import Bot

TELEGRAM_TOKEN = 'your_bot_token'
CHAT_ID = 'your_chat_id'

def send_alert(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

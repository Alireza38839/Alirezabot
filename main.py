import telebot
import re

API_TOKEN = '7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8'
bot = telebot.TeleBot(API_TOKEN)

# هندلر برای دستور /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سلام! لینک پست اینستاگرام رو بفرست تا لینک دانلودشو بدم 👇")

# هندلر برای هر پیام متنی
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text
    # بررسی اینکه آیا لینک اینستاگرام هست یا نه
    if "instagram.com" in text:
        # لینک نمونه (فعلاً واقعی نیست)
        download_link = "https://example.com/download?url=" + text
        bot.reply_to(message, f"لینک دانلود آماده‌ست:\n{download_link}")
    else:
        bot.reply_to(message, "لطفاً لینک یک پست اینستاگرام بفرست.")

print("ربات روشن است...")
bot.infinity_polling()

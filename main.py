import telebot

API_TOKEN = '7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من آماده‌ام.")

print("ربات روشن است...")
bot.infinity_polling()

import telebot
import requests

BOT_TOKEN = '7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8'
bot = telebot.TeleBot(BOT_TOKEN)

def get_instagram_download_link(insta_url):
    api = 'https://insta-downloader-api.vercel.app/api?url='
    res = requests.get(api + insta_url).json()
    if 'media' in res:
        return res['media']
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! لینک پست اینستاگرام رو بفرست تا لینک دانلودش رو بدم 🎥

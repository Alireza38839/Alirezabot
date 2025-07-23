import telebot
import requests

BOT_TOKEN = '7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8'
bot = telebot.TeleBot(BOT_TOKEN)

CHANNEL_ID = -1002134567890  # آیدی عددی کانال mozikamx

def get_instagram_download_link(insta_url):
    api = 'https://insta-downloader-api.com?url='
    res = requests.get(api + insta_url).json()
    if 'media' in res:
        return res['media']
    return None

def is_user_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! لینک پست اینستاگرام رو بفرست تا لینک دانلود بدم ✨")

@bot.message_handler(func=lambda message: True)
def handle_instagram_link(message):
    if not is_user_member(message.from_user.id):
        bot.reply_to(message, "⛔️ برای استفاده از ربات، اول باید عضو کانال ما بشی:\n👉 https://t.me/mozikamx")
        return

    link = get_instagram_download_link(message.text)
    if link:
        bot.reply_to(message, f"✅ لینک دانلود:\n{link}")
    else:
        bot.reply_to(message, "❌ مشکلی در گرفتن لینک به وجود اومد. مطمئن شو لینک اینستاگرام درسته.")

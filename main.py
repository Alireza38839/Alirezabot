
import logging
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# توکن ربات تلگرام شما
BOT_TOKEN = "7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# تابع استخراج لینک ویدیو از اینستاگرام
def get_instagram_video_url(insta_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(insta_url, headers=headers)
        if 'video_url' in response.text:
            match = re.search(r'"video_url":"([^"]+)"', response.text)
            if match:
                video_url = match.group(1).replace("\\u0026", "&").replace("\\", "")
                return video_url
        return None
    except Exception as e:
        return None

# تابع پاسخ به پیام کاربر
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "instagram.com" in text:
        await update.message.reply_text("⏳ در حال استخراج لینک ویدیو...")
        video_url = get_instagram_video_url(text)
        if video_url:
            await update.message.reply_text(f"✅ لینک دانلود مستقیم:\n{video_url}")
        else:
            await update.message.reply_text("❌ نتونستم لینک ویدیو رو پیدا کنم.")
    else:
        await update.message.reply_text("لطفا لینک پست اینستاگرام رو بفرست 😊")

# راه‌اندازی ربات
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

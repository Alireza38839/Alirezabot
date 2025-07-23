from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8"
ADMIN_ID = 8015247368

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("سلام! لینک اینستاگرام بفرست تا لینک دانلود بدم 🎥")

def is_instagram_url(text):
    return "instagram.com" in text and ("reel" in text or "p" in text or "tv" in text)

def fetch_download_link(insta_url):
    try:
        api_url = f"https://api.instasupersave.com/instasaver?url={insta_url}"
        r = requests.get(api_url, timeout=10)
        data = r.json()
        if 'media' in data and isinstance(data['media'], list) and len(data['media']) > 0:
            return data['media'][0].get('url')
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = update.message.text.strip()
    if is_instagram_url(text):
        await update.message.reply_text("🔄 در حال دریافت لینک دانلود...")
        download_link = fetch_download_link(text)
        if download_link:
            await update.message.reply_text(f"✅ لینک دانلود:\n{download_link}")
        else:
            await update.message.reply_text("❌ مشکلی در دریافت لینک پیش اومد. دوباره امتحان کن.")
    else:
        await update.message.reply_text("⛔ لطفاً لینک معتبر اینستاگرام بفرست.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ربات روشن شد ✅")
    app.run_polling()

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک پست اینستاگرام رو بفرست تا لینک دانلودشو بدم 😎")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "instagram.com" in text:
        await update.message.reply_text("⏳ در حال دریافت لینک دانلود...")

        api_url = "https://saveig.app/api/ajaxSearch"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "q": text,
            "t": "media",
            "lang": "en"
        }

        try:
            response = requests.post(api_url, data=data, headers=headers).json()
            if response.get("status") == "ok":
                media = response.get("medias", [])[0]
                download_link = media.get("url")
                await update.message.reply_text(f"✅ لینک دانلود:\n{download_link}")
            else:
                await update.message.reply_text("❌ مشکلی پیش اومد. مطمئن شو لینک درسته.")
        except Exception as e:
            await update.message.reply_text(f"❌ خطا: {e}")
    else:
        await update.message.reply_text("لینک معتبر اینستاگرام بفرست :)")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

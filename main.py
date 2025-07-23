from insta_downloader import extract_instagram_video
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک پست یا ویدیوی اینستاگرام رو بفرست تا لینکشو بدم 🎬")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "instagram.com" in text:
        await update.message.reply_text("⏳ در حال پردازش لینک...")
        try:
            video_url = extract_instagram_video(text)
            await update.message.reply_text(f"✅ لینک دانلود:\n{video_url}")
        except Exception as e:
            await update.message.reply_text("❌ خطایی در پردازش لینک رخ داد.")
            print("Error:", e)
    else:
        await update.message.reply_text("لطفاً یه لینک معتبر اینستاگرام بفرست 🌐")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

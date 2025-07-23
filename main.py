import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from instagrapi import Client

# ساختار برای ذخیره اطلاعات کاربران
users = {}

# شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📥 ورود به اینستاگرام", callback_data="login")],
        [InlineKeyboardButton("🎞️ ارسال لینک ریلز", callback_data="send_link")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("به ربات اینستا‌دانلودر خوش اومدی! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

# مدیریت دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "login":
        await query.message.reply_text("لطفاً یوزرنیم و پسورد اینستای خود را به صورت زیر ارسال کن:\n\n`username|password`", parse_mode="Markdown")
        users[query.from_user.id] = {"step": "login"}

    elif query.data == "send_link":
        if query.from_user.id in users and "client" in users[query.from_user.id]:
            await query.message.reply_text("لطفاً لینک ریلز اینستاگرام را ارسال کن:")
            users[query.from_user.id]["step"] = "get_link"
        else:
            await query.message.reply_text("❌ ابتدا باید وارد حساب اینستاگرام شوید.")

# مدیریت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # ورود
    if user_id in users and users[user_id].get("step") == "login":
        try:
            username, password = text.split("|")
            cl = Client()
            cl.login(username, password)
            users[user_id]["client"] = cl
            users[user_id]["step"] = None
            await update.message.reply_text("✅ ورود موفقیت‌آمیز بود! حالا لینک ریلز را ارسال کنید.")
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در ورود: {e}")

    # دریافت لینک ریلز
    elif user_id in users and users[user_id].get("step") == "get_link":
        try:
            cl = users[user_id]["client"]
            media = cl.media_info_from_url(text)
            url = cl.media_pk_to_url(media.pk)
            await update.message.reply_text(f"✅ لینک دانلود:\n{url}")
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در دریافت لینک: {e}")
        users[user_id]["step"] = None

    else:
        await update.message.reply_text("دستور نامعتبر. از دکمه‌ها استفاده کن.")

# راه‌اندازی بات
async def main():
    app = ApplicationBuilder().token("7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 ربات با موفقیت اجرا شد...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

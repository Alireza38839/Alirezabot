from telebot import TeleBot, types
import json

BOT_TOKEN = "7956280947:AAFGEAIx35DLrVSxkaqnKu1KhOsV9WUkYw8"
CHANNEL_ID = "@mozikamx"  # این رو با ای‌دی کانال خودت جایگزین کن
OWNER_ID = 8015247368

bot = TeleBot(BOT_TOKEN)
USERS_DB = "users.json"

def save_user(user_id):
    try:
        with open(USERS_DB, "r") as f:
            users = json.load(f)
    except:
        users = []
    if user_id not in users:
        users.append(user_id)
        with open(USERS_DB, "w") as f:
            json.dump(users, f)

def is_user_member(user_id):
    try:
        st = bot.get_chat_member(CHANNEL_ID, user_id).status
        return st in ["member","creator","administrator"]
    except:
        return False

def get_video_link(insta_url):
    # این تابع رو با تابع واقعی خودت جایگزین کن
    return "https://example.com/real-video.mp4"

@bot.message_handler(commands=['start'])
def cmd_start(m):
    save_user(m.from_user.id)
    if not is_user_member(m.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("➕ عضویت در کانال", url=f"https://t.me/{CHANNEL_ID.strip('@')}"))
        bot.reply_to(m, "برای شروع لطفاً ابتدا در کانال عضو شو:", reply_markup=markup)
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👥 تعداد کاربران", callback_data="user_count"))
    bot.reply_to(m, "سلام! لینک اینستاگرامت رو بفرست تا لینک دانلودش رو دریافت کنی.", reply_markup=markup)

@bot.message_handler(func=lambda msg:"instagram.com" in msg.text)
def handle_insta(m):
    if not is_user_member(m.from_user.id):
        return cmd_start(m)
    link = get_video_link(m.text.strip())
    if link:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("دانلود ویدیو 🎬", url=link))
        bot.reply_to(m, "ویدیو آماده‌ست:", reply_markup=markup)
    else:
        bot.reply_to(m, "❌ لینک دانلود پیدا نشد.")

@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    if call.data=="user_count":
        cnt = 0
        try:
            with open(USERS_DB,"r") as f:
                cnt = len(json.load(f))
        except:
            pass
        bot.answer_callback_query(call.id, f"👥 کاربران ربات: {cnt} نفر")

if __name__=="__main__":
    print("Bot starting...")
    bot.infinity_polling()

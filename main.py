from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    CallbackQueryHandler
)
import os

# ✅ Admin Telegram ID
ADMIN_ID = 7155245576  # မင်း admin ID ထား

# ✅ Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "💰 Member ဝင်ကြေး – 2,000 MMK\n\n"
        "📲 ပေးပို့ရန်နည်းလမ်းများ:\n\n"
        "✅ WavePay / KBZPay\n"
        "📌 09891947437\n"
        "👤 Name – U Chit San Mg\n\n"
        "✅ MPT Pay / ATOM Pay\n"
        "📌 Phone Bill Payment\n"
        "📸 Screenshot နဲ့ နံပါတ် (Phone Number) ကိုတစ်ခါတည်းရေးပြီး ပေးပို့ပေးပါ။\n\n"
        "⚠️ ပေးပြီးပါက Screenshot ပေးပို့ပါ။ Admin စစ်ဆေးပြီး access ပေးပါမယ်။"
    )

# ✅ Screenshot ပေးတဲ့အခါ Admin ကို ပြ
async def handle_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo = update.message.photo[-1].file_id
    caption = f"📥 Screenshot from @{user.username or user.id} (ID: {user.id})"

    keyboard = [
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Admin ထံသို့ Screenshot ပေးပို့
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption,
        reply_markup=reply_markup
    )

    await update.message.reply_text("📤 Screenshot ပေးပြီးပါပြီ – Admin စစ်ဆေးနေပါတယ်။")

# ✅ Admin Button ကို နှိပ်တဲ့အခါ
async def approve(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    user_id = int(query.data.split('_')[1])

    await context.bot.send_message(
        chat_id=user_id,
        text="✅ မင်္ဂလာပါ – သင်သည် Member ဖြစ်ပြီး အသုံးပြုနိုင်ပါပြီ။"
    )

    await query.edit_message_caption(caption="✅ Approved by Admin")

# ✅ Main Bot Run Function
def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        print("❌ BOT_TOKEN not found. Please set it in Railway Variables.")
        return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(approve, pattern="^approve_"))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# অনুমোদিত Telegram User ID
ALLOWED_USERS = {
    int(x.strip())
    for x in os.getenv("ALLOWED_USERS", "").split(",")
    if x.strip()
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ আপনার এই বট ব্যবহারের অনুমতি নেই।")
        return

    await update.message.reply_text(
        "✅ আপনি অনুমোদিত।\n\n"
        "ফাইলের message ID দিয়ে ব্যবহার করুন:\n"
        "/get MESSAGE_ID"
    )


async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ অনুমতি নেই।")
        return

    if not CHANNEL_ID:
        await update.message.reply_text("❌ CHANNEL_ID সেট করা হয়নি।")
        return

    if not context.args:
        await update.message.reply_text(
            "ব্যবহার করুন:\n/get MESSAGE_ID"
        )
        return

    try:
        message_id = int(context.args[0])

        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=int(CHANNEL_ID),
            message_id=message_id
        )

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "❌ ফাইলটি পাওয়া যায়নি বা পাঠানো সম্ভব হয়নি।"
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN পাওয়া যায়নি")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", get_file))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

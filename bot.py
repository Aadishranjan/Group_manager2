# --- Flask server for Render/Heroku ---
from flask import Flask
import threading
import os

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running!"

def run_server():
    port = int(os.getenv("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# --- Telegram Bot Setup ---
import asyncio
import logging
import sys
import traceback
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from config import BOT_TOKEN, ADMIN_ID
from plugins.function import start
from plugins.cleanservices import delete_service_messages
from plugins.wordfilter import addword, badwords, filter_bad_words


async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/broadcast - Only bot admin is allowed\n"
        "/ban - Ban a user\n"
        "/unban - Unban a user\n"
        "/mute - Mute a user\n"
        "/unmute - Unmute a user\n"
        "/warn - Tag a user or use /warn @username to warn them\n"
        "Users will be banned after 3 warnings."
    )

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()

        # Handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, delete_service_messages))
        app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, delete_service_messages))
        app.add_handler(MessageHandler(filters.StatusUpdate.VIDEO_CHAT_STARTED, delete_service_messages))
        app.add_handler(MessageHandler(filters.StatusUpdate.VIDEO_CHAT_ENDED, delete_service_messages))
        app.add_handler(CommandHandler("addword", addword))
        app.add_handler(CommandHandler("badwords", badwords))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_bad_words))

        print("✅ Bot is running...")
        app.run_polling()

    except Exception:
        error_text = f"🚨 BOT CRASHED!\n\n{traceback.format_exc()}"
        logging.error(error_text)

        async def notify_admin():
            try:
                bot = Bot(BOT_TOKEN)
                await bot.send_message(chat_id=ADMIN_ID, text=error_text)
            except Exception as notify_err:
                print(f"Error notifying admin: {notify_err}")

        asyncio.run(notify_admin())
        sys.exit(1)

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    main()
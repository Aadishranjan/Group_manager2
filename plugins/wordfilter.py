from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from database.badwords_db import add_bad_word, get_bad_words

BOT_OWNER_ID = int(5782873898)

# Delete bad words in message
async def filter_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return
    chat_id = msg.chat.id
    msg_text = msg.text.lower()
    words = get_bad_words(chat_id)

    if any(word in msg_text for word in words):
        try:
            await msg.delete()
        except:
            pass

# Add a word (only bot owner)
async def addword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID:
        await update.message.reply_text("❌ Only the bot owner can add bad words.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /addword <word>")
        return

    word = context.args[0]
    add_bad_word(update.effective_chat.id, word)
    await update.message.reply_text(f"✅ Added `{word}` to bad words list.", parse_mode="Markdown")

# View word list (only bot owner)
async def badwords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID:
        await update.message.reply_text("❌ Only the bot owner can view bad words.")
        return

    words = get_bad_words(update.effective_chat.id)
    if not words:
        await update.message.reply_text("✅ No bad words set.")
    else:
        msg = "**Bad Words List:**\n" + "\n".join(f"- `{w}`" for w in words)
        await update.message.reply_text(msg, parse_mode="Markdown")
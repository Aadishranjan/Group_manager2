import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

logger = logging.getLogger(__name__)

async def delete_service_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message:
            await update.message.delete()
    except Exception as e:
        logger.warning(f"Failed to delete service message: {e}")
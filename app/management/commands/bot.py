from django.core.management.base import BaseCommand
import logging
from django.conf import settings
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, CallbackQueryHandler

updater = Updater(token=settings.TELEGRAM_BOT_TOKEN)
dispatcher = updater.dispatcher

class Command(BaseCommand):
    help = 'Start telegram bot'

    def handle(self, *args, **kwargs):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        
        import app.bot.register_profile
        
        updater.start_polling()
        updater.idle()

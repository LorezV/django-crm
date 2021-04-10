from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from app.management.commands.bot import updater, dispatcher
from app import models
print(f'@ - {__name__} imported')

keyboard_check_profile = [
    [InlineKeyboardButton('Проверить статус заявки 🔄', callback_data='button_update')],
    []
]

keyboard_manage_profile = [
    [InlineKeyboardButton('Мои заказы 🧐', callback_data='button_myorders'), InlineKeyboardButton('Обновить данные 🔄', callback_data='button_update')],
    []
]

def insert_profile(update, context, profile):
    return f'Личный кабинет: {profile.telegram_first_name} {profile.telegram_last_name} 🆔{profile.telegram_chat_id}\n\nОткрыто {profile.orders.count()} заказ(-ов)'

def cmd_start(update, context):
    profile = models.TelegramProfile.objects.filter(
        telegram_chat_id=update.effective_chat.id).first()
    if profile:
        if not profile.is_master and not profile.is_operator:
            update.effective_message.reply_text('Вашу заявку еще не одобрили. Пожалуйста, подождите еще чуть-чуть 🙂.', reply_markup=InlineKeyboardMarkup(keyboard_check_profile))
        else:
            update.effective_message.reply_text(insert_profile(update, context, profile), reply_markup=InlineKeyboardMarkup(keyboard_manage_profile))
    else:
        new_profile = models.TelegramProfile.objects.create(
            telegram_chat_id=update.effective_chat.id,
            telegram_first_name=update.effective_chat.first_name,
            telegram_last_name=update.effective_chat.last_name,
            telegram_username=update.effective_chat.username
        )
        update.message.reply_text(
            f'✔ У вас еще нет профиля в системе, но я отправил заявку на его создание😊. Пожалуйста, дождитесь пока оператор её примет.\nСохраненные данные:\n - @{new_profile.telegram_username}\n - {new_profile.telegram_first_name} {new_profile.telegram_last_name}',
            reply_markup=InlineKeyboardMarkup(keyboard_check_profile))

def keyboard_handler(update, context):
    update.callback_query.answer()
    profile = models.TelegramProfile.objects.filter(telegram_chat_id=update.effective_chat.id).first()
    if profile and (profile.is_operator or profile.is_master):
        if update.callback_query.data == 'button_update':
                try:
                    update.effective_message.edit_text(insert_profile(update, context, profile), reply_markup=InlineKeyboardMarkup(keyboard_manage_profile))
                except Exception as ex:
                    print(ex)
        elif update.callback_query.data == 'button_myorders':
            # Send orders cards
            pass


dispatcher.add_handler(CommandHandler('start', cmd_start))
dispatcher.add_handler(CallbackQueryHandler(keyboard_handler))

from app import models
from app.management.commands.bot import updater
from app.bot.bot_utils import insert_profile
from app.bot import keyboards
from app.bot.bot_utils import get_chat_data_or_none

def cmd_start(update, context):
    profile= models.TelegramProfile.objects.filter(
        telegram_chat_id = update.effective_chat.id).first()
    if profile:
        if not profile.is_master and not profile.is_operator:
            edit_or_create_profile_message(context=context, text='Вашу заявку еще не одобрили. Пожалуйста, подождите еще чуть-чуть 🙂.', chat_id=update.effective_chat.id, reply_markup = InlineKeyboardMarkup(keyboards.keyboard_profile_check))
        else:
            edit_or_create_profile_message(context=context, text=insert_profile(update, context, profile), chat_id=update.effective_chat.id, reply_markup = keyboards.get_profile_keyboard(profile))
    else:
        new_profile=models.TelegramProfile.objects.create(
            telegram_chat_id=update.effective_chat.id,
            telegram_first_name=update.effective_chat.first_name,
            telegram_last_name=update.effective_chat.last_name,
            telegram_username=update.effective_chat.username
        )
        edit_or_create_profile_message(context=context, text=f'✔ У вас еще нет профиля в системе, но я отправил заявку на его создание😊. Пожалуйста, дождитесь пока оператор её примет.\nСохраненные данные:\n - @{new_profile.telegram_username}\n - {new_profile.telegram_first_name} {new_profile.telegram_last_name}', chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboards.keyboard_profile_check))

def edit_or_create_profile_message(context, text, chat_id=None, parse_mode=None, reply_markup=None):
    message_id = get_chat_data_or_none(context, 'profile_message_id')
    if message_id:
        updater.bot.editMessageText(text, chat_id=chat_id, message_id=message_id, parse_mode=parse_mode, reply_markup=reply_markup)
    else:
        msg = updater.bot.sendMessage(text, chat_id=chat_id, message_id=message_id, parse_mode=parse_mode, reply_markup=reply_markup)
        contex.chat_data['profile_message_id'] = msg.message_id
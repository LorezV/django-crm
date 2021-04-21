from app import models
from app.management.commands.bot import updater
from app.bot.bot_utils import insert_profile
from app.bot import keyboards
from app.bot.bot_utils import get_chat_data_or_none
from telegram import InlineKeyboardMarkup

def cmd_start(update, context):
    profile= models.TelegramProfile.objects.filter(
        telegram_chat_id = update.effective_chat.id).first()
    if profile:
        if not profile.is_master and not profile.is_operator:
            update.effective_message.reply_text(
                'Вашу заявку еще не одобрили. Пожалуйста, подождите еще чуть-чуть 🙂.', reply_markup = InlineKeyboardMarkup(keyboards.keyboard_profile_check))
        else:
            update.effective_message.reply_text(insert_profile(
                update, context, profile), reply_markup = keyboards.get_profile_keyboard(profile))
    else:
        new_profile=models.TelegramProfile.objects.create(
            telegram_chat_id=update.effective_chat.id,
            telegram_first_name=update.effective_chat.first_name,
            telegram_last_name=update.effective_chat.last_name,
            telegram_username=update.effective_chat.username
        )
        update.effective_message.reply_text(
            f'✔ У вас еще нет профиля в системе, но я отправил заявку на его создание😊. Пожалуйста, дождитесь пока оператор её примет.\nСохраненные данные:\n - @{new_profile.telegram_username}\n - {new_profile.telegram_first_name} {new_profile.telegram_last_name}',
            reply_markup=InlineKeyboardMarkup(keyboards.keyboard_profile_check))
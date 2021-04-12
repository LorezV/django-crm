from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from app.management.commands.bot import updater, dispatcher
from app import models
import re

keyboard_check_profile = [
    [InlineKeyboardButton('Проверить статус заявки 🔄', callback_data='button_update')],
    []
]

keyboard_manage_profile = [
    [InlineKeyboardButton('Мои заказы 🧐', callback_data='button_myorders'), InlineKeyboardButton(
        'Обновить данные 🔄', callback_data='button_update')],
    []
]

keyboard_order_manage = [
    [
        InlineKeyboardButton('Закрыть заказ ✅', callback_data='order_button_close'),
        InlineKeyboardButton('Отменить заказ ❌', callback_data='order_button_cancel'),
        InlineKeyboardButton('🔧', callback_data='order_button_modern')
    ],
    [
        InlineKeyboardButton('Установить цену 💸', callback_data='order_button_amount'),
        InlineKeyboardButton('Прокомментировать 💬', callback_data='order_button_comment'),
    ],
    [
        InlineKeyboardButton('Обновить данные 🔄',callback_data='order_button_update'),
    ],
    [
        InlineKeyboardButton('Назад', callback_data='open_order_tabs_layout'),
    ],
]

keyboard_order_tabs = [
    [InlineKeyboardButton('Управление ⚙', callback_data='open_order_manage_layout')],
    [InlineKeyboardButton('Обновить данные 🔄',callback_data='order_button_update')],
    [InlineKeyboardButton('➖', callback_data='order_hide')]
]

def valid_order_comment(order):
    if not order.master_comment:
        return False
    return True

def valid_order_amount(order):
    if order.amount <= 0:
        return False
    return True

def valid_order(order):
    if order.amount <= 0:
        return False
    if not order.master_comment:
        return False
    return True

def insert_profile(update, context, profile):
    return f'Личный кабинет: {profile.telegram_first_name} {profile.telegram_last_name} 🆔{profile.telegram_chat_id}\n\nОткрыто {profile.orders.filter(order_status__regex=r"W|J|M").count()} заказ(-ов)'


def insert_order(update, context, order):
    message= f'#{order.id}\nНачать нужно: {order.working_date} 🕗\nИнформация о клиенте:\n - {order.client_name}\n - {order.client_phone}\n - {order.client_adress},{order.client_city},\n - {order.status_verbose}/{order.type_verbose}\n - {order.comment}'
    if valid_order_amount(order):
        message += f'\nЦена: {order.amount}'
    else:
        message += '\n\n⚠ Установите правильную цену за заказ.'
    if valid_order_comment(order):
        message += f'\nВаш комментарий: {order.master_comment}'
    else:
        message += '\n⚠ Прокомментируйте заказ.'
    return message


def delete_message_to_delete(update, context):
    try:
        updater.bot.deleteMessage(update.effective_chat.id, int(context.chat_data['message_to_delete']))
        context.chat_data['message_to_delete'] = None
    except Exception as e:
        print(e)


def cmd_start(update, context):
    profile= models.TelegramProfile.objects.filter(
        telegram_chat_id = update.effective_chat.id).first()
    if profile:
        if not profile.is_master and not profile.is_operator:
            update.effective_message.reply_text(
                'Вашу заявку еще не одобрили. Пожалуйста, подождите еще чуть-чуть 🙂.', reply_markup = InlineKeyboardMarkup(keyboard_check_profile))
        else:
            update.effective_message.reply_text(insert_profile(
                update, context, profile), reply_markup = InlineKeyboardMarkup(keyboard_manage_profile))
    else:
        new_profile=models.TelegramProfile.objects.create(
            telegram_chat_id=update.effective_chat.id,
            telegram_first_name=update.effective_chat.first_name,
            telegram_last_name=update.effective_chat.last_name,
            telegram_username=update.effective_chat.username
        )
        update.effective_message.reply_text(
            f'✔ У вас еще нет профиля в системе, но я отправил заявку на его создание😊. Пожалуйста, дождитесь пока оператор её примет.\nСохраненные данные:\n - @{new_profile.telegram_username}\n - {new_profile.telegram_first_name} {new_profile.telegram_last_name}',
            reply_markup=InlineKeyboardMarkup(keyboard_check_profile))


def user_response_handler(update, context):
    if update.message:
        pass
    elif update.callback_query:
        query = update.callback_query
        data = query.data
        profile = models.TelegramProfile.objects.filter(telegram_chat_id=update.effective_chat.id).first()

        if profile and (profile.is_operator or profile.is_master):
            if data == 'button_update':
                try:
                    update.effective_message.edit_text(insert_profile(update, context, profile), reply_markup=InlineKeyboardMarkup(keyboard_manage_profile))
                except Exception as ex:
                    print(ex)
            elif data == 'button_myorders':
                for order in profile.orders.filter(order_status__regex=r'W|J|M'):
                    update.effective_message.reply_text(insert_order(update, context, order), reply_markup=InlineKeyboardMarkup(keyboard_order_tabs))
            else:
                order = models.Order.objects.filter(id=re.search(r'#([1-9]+)', update.effective_message.text).group(1)).first()
                if order:
                    context.chat_data['order'] = order
                    if data == 'order_button_amount':
                        msg = update.effective_message.reply_text(f'Укажите цену заказа #{order.id} 💰💰💰')
                        context.chat_data['message_to_delete'] = msg.message_id
                        return 'ask_order_amount'
                    elif data == 'order_hide':
                        update.effective_message.delete()
                    elif data == 'order_button_comment':
                        msg = update.effective_message.reply_text(f'Напишите комментарий к заказу #{order.id} 💬💬💬')
                        context.chat_data['message_to_delete'] = msg.message_id
                        return 'ask_order_comment'
                    elif data == 'order_button_modern':
                            order.order_status = 'M'
                            order.save()
                            update.effective_message.edit_text(insert_order(update, context, order), reply_markup=InlineKeyboardMarkup(keyboard_order_manage))
                    elif data == 'open_order_manage_layout':
                        update.effective_message.edit_text(insert_order(update, context, order), reply_markup=InlineKeyboardMarkup(keyboard_order_manage))
                    elif data == 'open_order_tabs_layout':
                        update.effective_message.edit_text(insert_order(update, context, order), reply_markup=InlineKeyboardMarkup(keyboard_order_tabs))
                    elif data == 'order_button_update':
                        try:
                            update.effective_message.edit_text(insert_order(update, context, order), reply_markup=InlineKeyboardMarkup(keyboard_order_tabs))
                        except Exception as ex:
                            print(ex)
                    elif data == 'order_button_cancel':
                        if valid_order_comment(order):
                            order.order_status = 'C'
                            order.save()
                            update.effective_message.delete()
                            updater.bot.sendMessage(update.effective_chat.id, f'Вы отменили заказ #{order.id} ❌😑')
                        else:
                            try:
                                update.effective_message.edit_text(insert_order(update, context, order), reply_markup=InlineKeyboardMarkup(keyboard_order_manage))
                            except Exception as e:
                                print(e)
                    elif data == 'order_button_close':
                        if valid_order(order):
                            order.order_status = 'R'
                            order.save()
                            update.effective_message.delete()
                            updater.bot.sendMessage(update.effective_chat.id, f'Заказ #{order.id} успешно закрыт 😄😉')
                        else:
                            try:
                                update.effective_message.edit_text(insert_order(update, context, order), reply_markup=InlineKeyboardMarkup(keyboard_order_manage))
                            except Exception as e:
                                print(e)
    return ConversationHandler.END

def ask_order_amount(update, context):
    amount = update.effective_message.text
    order = context.chat_data['order']
    order.amount = amount
    order.save()
    update.effective_message.delete()
    delete_message_to_delete(update, context)
    return ConversationHandler.END

def ask_order_comment(update, context):
    comment = update.effective_message.text
    order = context.chat_data['order']
    order.master_comment = comment
    order.save()
    update.effective_message.delete()
    delete_message_to_delete(update, context)
    return ConversationHandler.END

conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(user_response_handler)],
    states={
        'ask_order_amount': [MessageHandler(Filters.regex('^[0-9]+$'), ask_order_amount)],
        'ask_order_comment': [MessageHandler(Filters.text, ask_order_comment)]
    },
    fallbacks=[CallbackQueryHandler(user_response_handler)],
)


dispatcher.add_handler(CommandHandler('start', cmd_start))
dispatcher.add_handler(conversation)

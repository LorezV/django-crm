from app.management.commands.bot import updater
from app.bot import keyboards
import humanize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def insert_order(order):
    message = f""" 
Заказ <b>#{order.id}</b>
Информация:
 🕗 {order._meta.get_field('working_date').verbose_name}: <b>{order.working_date}</b>
 👤 {order._meta.get_field('client_name').verbose_name}: <b>{order.client_name}</b>
 💁 {order._meta.get_field('master_advert_name').verbose_name}: <b>{order.master_advert_name}</b>
 ☎ {order._meta.get_field('client_phone').verbose_name}: <b>{order.client_phone}</b>
 🌍 {order._meta.get_field('client_city').verbose_name}: <b>{order.client_city}</b>
 🏡 {order._meta.get_field('client_adress').verbose_name}: <b>{order.client_adress}</b>
 🔍 {order._meta.get_field('order_type').verbose_name}: <b>{order.type_verbose}</b>
 💰 {order._meta.get_field('announced_amounts').verbose_name}:   <b>{order.announced_amounts}</b>
 💬 {order._meta.get_field('comment').verbose_name}: <b>{order.comment}</b>
""" 
    return message

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

def get_chat_data_or_none(context, field_name):
    try:
        return context.chat_data[field_name]
    except Exception:
        return None

def delete_message_to_delete(update, context):
    try:
        msg_id = int(get_chat_data_or_none(context, 'message_to_delete'))
        if msg_id:
            updater.bot.deleteMessage(update.effective_chat.id, int(msg_id))
        context.chat_data['message_to_delete'] = None
    except Exception as e:
        print(e)

def insert_profile(update, context, profile):
    return f'Личный кабинет: {profile.telegram_first_name} {profile.telegram_last_name} 🆔{profile.telegram_chat_id}\n\nОткрыто {profile.orders.filter(order_status__regex=r"W|J|M").count()} заказ(-ов)'


def insert_order_manage(update, context, order):
    message = insert_order(order)
    if valid_order_amount(order):
        message += f'\nЦена: {humanize.intcomma(order.amount)} ₽'
    else:
        message += '\n\n⚠ Установите правильную цену за заказ.'
    if valid_order_comment(order):
        message += f'\nВаш комментарий: {order.master_comment}'
    else:
        message += '\n⚠ Прокомментируйте заказ.'
    return message

def insert_create_order_form(update, context):
    message = f"""
Город: <b>{get_chat_data_or_none(context, 'form_client_city')}</b>
Адрес: <b>{get_chat_data_or_none(context, 'form_client_adress')}</b>
Имя клиента: <b>{get_chat_data_or_none(context, 'form_client_name')}</b>
Телефон клиента: <b>{get_chat_data_or_none(context, 'form_client_phone')}</b>
Проблема: <b>{get_chat_data_or_none(context, 'form_client_comment')}</b>
Имя из рекламы: <b>{get_chat_data_or_none(context, 'form_adver_name')}</b>
Тип: <b>{get_chat_data_or_none(context, 'form_order_type')}</b>
Цены озвучены: <b>{get_chat_data_or_none(context, 'form_order_announced_amounts')}</b>
Мастера: <b>{get_chat_data_or_none(context, 'form_order_masters')}</b>
"""
    return message
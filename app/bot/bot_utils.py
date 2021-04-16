from app.management.commands.bot import updater
from app.bot import keyboards

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

def offer_master_order(telegram_chat_id, order):
    try:
        message = '💼 Вам поступило новое предложение'
        message += insert_order(order)
        updater.bot.sendMessage(telegram_chat_id, message, reply_markup=keyboards.get_offer_order_keyboard(), parse_mode='html')
    except Exception as e:
        print(e)
from app.management.commands.bot import updater
from app.bot.bot_utils import insert_order
from app.bot import keyboards

def offer_master_order(master, order):
    try:
        message = '💼 Вам поступил новый заказ'
        message += insert_order(order)
        updater.bot.sendMessage(master.telegram_chat_id, message, reply_markup=keyboards.get_offer_order_keyboard(), parse_mode='html')
    except Exception as e:
        print(e)
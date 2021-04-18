from app.management.commands.bot import updater
from app.bot.bot_utils import insert_order
from app.bot import keyboards

# def remove_job_if_exists(name, context):
#     current_jobs = context.job_queue.get_jobs_by_name(name)
#     if not current_jobs:
#         return False
#     for job in current_jobs:
#         job.schedule_removal()
#     return True

# def set_timer(update, context):
#     chat_id = update.message.chat_id
#     try:
#         due = int(context.args[0])
#         if due < 0:
#             update.message.reply_text(
#                 'Извините, не умеем возвращаться в прошлое')
#             return

#         job_removed = remove_job_if_exists(
#             str(chat_id), 
#             context
#         )
#         context.job_queue.run_once(
#             task,
#             due,
#             context=chat_id,
#             name=str(chat_id)
#         )
#         text = f'Вернусь через {due} секунд!'
#         if job_removed:
#             text += ' Старая задача удалена.'
#         update.message.reply_text(text)

#     except (IndexError, ValueError):
#         update.message.reply_text('Использование: /set <секунд>')

# def task(context):
#     job = context.job
#     context.bot.send_message(job.context, text='Вернулся!')

# def unset_timer(update, context):
#     chat_id = update.message.chat_id
#     job_removed = remove_job_if_exists(str(chat_id), context)
#     text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера.'
#     update.message.reply_text(text)

def offer_master_order(master, order):
    try:
        message = '💼 Вам поступил новый заказ'
        message += insert_order(order)
        updater.bot.sendMessage(master.telegram_chat_id, message, reply_markup=keyboards.get_offer_order_keyboard(), parse_mode='html')
    except Exception as e:
        print(e)
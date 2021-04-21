from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext, \
    ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup
from app.management.commands.bot import updater, dispatcher
from telegram import InlineKeyboardButton, ReplyKeyboardRemove
from app.bot import keyboards, bot_utils
from app.bot.bot_utils import valid_order, valid_order_amount, \
    valid_order_comment, get_chat_data_or_none, delete_message_to_delete, \
    insert_order, insert_profile, insert_create_order_form, insert_order_manage
from app.bot.command_utils import cmd_start
import humanize
from app import models
from app import forms
from django.utils import timezone
import re


def go_create_order(update, context):
    msg_id = get_chat_data_or_none(context, 'order_creation_message_id')
    if msg_id:
        try:
            updater.bot.deleteMessage(update.effective_chat.id, int(msg_id))
        except Exception as e:
            print(e)
    context.chat_data[
        'order_creation_message_id'] = update.effective_message.reply_text(
        insert_create_order_form(updater, context),
        reply_markup=keyboards.get_create_order_keyboard(),
        parse_mode='html').message_id
    msg = update.effective_message.reply_text('Укажите город',
                                              reply_markup=keyboards.get_order_city_keyboard())
    context.chat_data['message_to_delete'] = msg.message_id


def send_master_orders(update, context, profile):
    for order in profile.orders.filter(order_status__regex=r'W|J|M'):
        update.effective_message.reply_text(
            insert_order_manage(update, context, order),
            reply_markup=InlineKeyboardMarkup(keyboards.keyboard_order_tabs),
            parse_mode='html')


def user_response_handler(update, context):
    try:
        profile = models.TelegramProfile.objects.filter(
            telegram_chat_id=update.effective_chat.id).first()
        humanize.i18n.activate("ru_RU")
        if update.message:
            if update.message.text == 'Форма создания заказа ➕':
                update.effective_message.reply_text('Создание заказа...',
                                                    reply_markup=ReplyKeyboardRemove())
                go_create_order(update, context)
                return ConversationHandler.END
            elif update.message.text == 'Мои заказы 🧐':
                send_master_orders(update, context, profile)
                return ConversationHandler.END
            else:
                update.effective_message.delete()
                try:
                    delete_message_to_delete(update, context)
                except Exception as e:
                    print(e)
        elif update.callback_query:
            query = update.callback_query
            data = query.data
            query.answer()
            if profile and (profile.is_operator or profile.is_master):
                if data == 'orderform_editform':
                    context.chat_data[
                        'order_creation_message_id'] = update.effective_message.message_id
                    try:
                        update.effective_message.edit_text(
                            insert_create_order_form(updater, context),
                            reply_markup=keyboards.get_create_order_keyboard(),
                            parse_mode='html')
                    except Exception as e:
                        print(e)
                    msg = update.effective_message.reply_text('Укажите город',
                                                              reply_markup=keyboards.get_order_city_keyboard())
                    context.chat_data['message_to_delete'] = msg.message_id
                elif data == 'orderform_submit':
                    client_name = get_chat_data_or_none(context,
                                                        'form_client_name')
                    advert_name = get_chat_data_or_none(context,
                                                        'form_adver_name')
                    adress = get_chat_data_or_none(context,
                                                   'form_client_adress')
                    phone = get_chat_data_or_none(context, 'form_client_phone')
                    city = models.City.objects.filter(
                        title=get_chat_data_or_none(context,
                                                    'form_client_city')).first()
                    order_type = get_chat_data_or_none(context,
                                                       'form_order_type')
                    comment = get_chat_data_or_none(context,
                                                    'form_client_comment')
                    input_masters = get_chat_data_or_none(context,
                                                          'form_order_masters')
                    announced_amounts = get_chat_data_or_none(context,
                                                              'form_order_announced_amounts')
                    masters = []
                    if input_masters:
                        for input_master in input_masters.split(', '):
                            master = models.TelegramProfile.objects.filter(
                                telegram_last_name=input_master).first()
                            if master:
                                masters.append(master)
                            else:
                                update.effective_message.reply_text(
                                    f'Мастер <b>{input_master}</b> не был найден.',
                                    parse_mode='html')
                    for row in models.Order.TypeChoice:
                        if order_type in row:
                            order_type = row[0]
                    new_order = forms.OrderCreateForm(
                        {'client_name': client_name,
                         "master_advert_name": advert_name,
                         'client_adress': adress, 'client_city': city,
                         'client_phone': phone, 'comment': comment,
                         "order_type": order_type,
                         'working_date': timezone.now() + timezone.timedelta(
                             hours=1, minutes=30), 'master_requests': masters,
                         'announced_amounts': announced_amounts})
                    if new_order.is_valid():
                        new_order = new_order.save()
                        new_order.save()
                        update.effective_message.reply_text(
                            f'Вы создали заказ #{new_order.id}',
                            reply_markup=keyboards.get_profile_keyboard(
                                profile))
                        update.effective_message.delete()
                        context.chat_data['order_creation_message_id'] = None
                    else:
                        update.effective_message.reply_text(
                            f'Вы ввели неверные данные',
                            reply_markup=InlineKeyboardMarkup([[
                                                                   InlineKeyboardButton(
                                                                       '➖',
                                                                       callback_data='hide_message')]]))
                    return 'state_askform'
                elif data.split("_")[0] == 'type-button':
                    value = data.split('_')[1]
                    return set_orderform_type(update, context, value)
                elif data.split('_')[0] == 'set-city':
                    return set_orderform_city(update, context,
                                              data.split('_')[1])
                elif data == 'hide_message':
                    update.effective_message.delete()
                    return ConversationHandler.END
                elif data == 'button_update':
                    update.effective_message.edit_text(
                        insert_profile(update, context, profile),
                        reply_markup=keyboards.get_profile_keyboard(profile))
                else:
                    order = models.Order.objects.filter(
                        id=re.search(r'#([1-9]+)',
                                     update.effective_message.text).group(
                            1)).first()
                    context.chat_data['order'] = order
                    if order:
                        context.chat_data[
                            'current_message_of_order'] = update.effective_message.message_id
                        if data == 'offer_accept':
                            if not order.master:
                                update.effective_message.reply_text(
                                    f'Вы приняли заказ #{order.id} 😀 Посмотреть ин-фу о закае можно в "Мои заказы"',
                                    reply_markup=keyboards.get_profile_keyboard(
                                        profile))
                                order.master = profile
                                order.order_status = 'J'
                                order.save()
                            else:
                                update.effective_message.reply_text(
                                    f'У заказа #{order.id} уже назначен мастер.😀',
                                    reply_markup=keyboards.get_profile_keyboard(
                                        profile))
                                updater.bot.deleteMessage(
                                    update.effective_chat.id,
                                    update.effective_message.message_id)
                        elif data == 'order_button_amount':
                            msg = update.effective_message.reply_text(
                                f'Укажите цену заказа #{order.id} 💰💰💰')
                            context.chat_data[
                                'message_to_delete'] = msg.message_id
                            return 'ask_order_amount'
                        elif data == 'order_button_comment':
                            msg = update.effective_message.reply_text(
                                f'Напишите комментарий к заказу #{order.id} 💬💬💬')
                            context.chat_data[
                                'message_to_delete'] = msg.message_id
                            return 'ask_order_comment'
                        elif data == 'order_button_modern':
                            order.order_status = 'M'
                            order.save()
                            update.effective_message.edit_text(
                                insert_order_manage(update, context, order),
                                reply_markup=InlineKeyboardMarkup(
                                    keyboards.keyboard_order_manage),
                                parse_mode='html')
                        elif data == 'open_order_manage_layout':
                            update.effective_message.edit_text(
                                insert_order_manage(update, context, order),
                                reply_markup=InlineKeyboardMarkup(
                                    keyboards.keyboard_order_manage),
                                parse_mode='html')
                        elif data == 'open_order_tabs_layout':
                            update.effective_message.edit_text(
                                insert_order_manage(update, context, order),
                                reply_markup=InlineKeyboardMarkup(
                                    keyboards.keyboard_order_tabs),
                                parse_mode='html')
                        elif data == 'order_button_update':
                            update.effective_message.edit_text(
                                insert_order_manage(update, context, order),
                                reply_markup=InlineKeyboardMarkup(
                                    keyboards.keyboard_order_tabs),
                                parse_mode='html')
                        elif data == 'order_button_cancel':
                            if valid_order(order):
                                order.order_status = 'C'
                                order.save()
                                update.effective_message.delete()
                                updater.bot.sendMessage(
                                    update.effective_chat.id,
                                    f'Вы отменили заказ #{order.id} ❌😑')
                            else:
                                update.effective_message.edit_text(
                                    insert_order_manage(update, context,
                                                        order),
                                    reply_markup=InlineKeyboardMarkup(
                                        keyboards.keyboard_order_manage),
                                    parse_mode='html')
                        elif data == 'order_button_close':
                            if valid_order(order):
                                order.order_status = 'R'
                                order.closing_date = timezone.now()
                                order.save()
                                update.effective_message.delete()
                                updater.bot.sendMessage(
                                    update.effective_chat.id,
                                    f'Заказ #{order.id} успешно закрыт 😄😉')
                            else:
                                update.effective_message.edit_text(
                                    insert_order_manage(update, context,
                                                        order),
                                    reply_markup=InlineKeyboardMarkup(
                                        keyboards.keyboard_order_manage),
                                    parse_mode='html')
        return ConversationHandler.END
    except Exception as e:
        print(e)
        return ConversationHandler.END


def ask_order_amount(update, context):
    amount = update.effective_message.text
    order = context.chat_data['order']
    order.amount = amount
    order.save()
    update.effective_message.delete()
    # try:
    #     updater.bot.editMessageText(insert_order_manage(update, context, order), reply_markup=InlineKeyboardMarkup(keyboards.keyboard_order_tabs), parse_mode='html', chat_id=update.effective_chat.id, message_id=get_chat_data_or_none(context, 'current_message_of_order'))
    # except Exception as e:
    #     print(e)
    delete_message_to_delete(update, context)
    return ConversationHandler.END


def ask_order_comment(update, context):
    comment = update.effective_message.text
    order = context.chat_data['order']
    order.master_comment = comment
    order.save()
    update.effective_message.delete()
    # try:
    #     updater.bot.editMessageText(insert_order_manage(update, context, order), reply_markup=InlineKeyboardMarkup(keyboards.keyboard_order_tabs), parse_mode='html', chat_id=update.effective_chat.id, message_id=get_chat_data_or_none(context, 'current_message_of_order'))
    # except Exception as e:
    #     print(e)
    delete_message_to_delete(update, context)
    return ConversationHandler.END


def ask_orderform_clientname(update, context):
    try:
        text = update.effective_message.text
        context.chat_data['form_client_name'] = text
        update.effective_message.delete()
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
        delete_message_to_delete(update, context)
        msg = update.effective_message.reply_text('Укажите телефон клиента')
        context.chat_data['message_to_delete'] = msg.message_id
    except Exception as e:
        print(e)
    return 'state_askform_phone'


def ask_orderform_advertname(update, context):
    try:
        text = update.effective_message.text
        context.chat_data['form_adver_name'] = text
        update.effective_message.delete()
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
        delete_message_to_delete(update, context)
        msg = update.effective_message.reply_text('Укажите тип заказа.',
                                                  reply_markup=keyboards.get_order_type_keyboard(
                                                      choices=models.Order.TypeChoice))
        context.chat_data['message_to_delete'] = msg.message_id
    except Exception as e:
        print(e)
    return 'state_askform_type'


def ask_orderform_adress(update, context):
    try:
        text = update.effective_message.text
        context.chat_data['form_client_adress'] = text
        update.effective_message.delete()
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
        delete_message_to_delete(update, context)
        msg = update.effective_message.reply_text('Введите имя клиента')
        context.chat_data['message_to_delete'] = msg.message_id
    except Exception as e:
        print(e)
    return 'state_askform_clientname'


def ask_orderform_phone(update, context):
    try:
        text = update.effective_message.text
        context.chat_data['form_client_phone'] = text
        update.effective_message.delete()
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
        delete_message_to_delete(update, context)
        msg = update.effective_message.reply_text('Опишите проблему')
        context.chat_data['message_to_delete'] = msg.message_id
    except Exception as e:
        print(e)
    return 'state_askform_comment'


def ask_orderform_city(update, context):
    try:
        text = update.effective_message.text
        context.chat_data['form_client_city'] = text
        update.effective_message.delete()
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
        delete_message_to_delete(update, context)
        msg = update.effective_message.reply_text('Укажите адрес клиента')
        context.chat_data['message_to_delete'] = msg.message_id
    except Exception as e:
        print(e)
    return 'state_askform_adress'


def ask_orderform_comment(update, context):
    try:
        text = update.effective_message.text
        context.chat_data['form_client_comment'] = text
        update.effective_message.delete()
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
        delete_message_to_delete(update, context)
        msg = update.effective_message.reply_text('Укажите рекламное имя ВМ')
        context.chat_data['message_to_delete'] = msg.message_id
    except Exception as e:
        print(e)
    return 'state_askform_advertname'


def ask_orderform_masters(update, context):
    profile = models.TelegramProfile.objects.filter(
        telegram_chat_id=update.effective_chat.id).first()
    try:
        text = update.effective_message.text
        context.chat_data['form_order_masters'] = text
        update.effective_message.delete()
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
        delete_message_to_delete(update, context)
    except Exception as e:
        print(e)
    update.effective_message.reply_text('Проверьте введённые данные еще раз!',
                                        reply_markup=keyboards.get_profile_keyboard(
                                            profile))
    return ConversationHandler.END


def set_orderform_type(update, context, value):
    try:
        for row in models.Order.TypeChoice:
            if value in row:
                value = row[1]
        context.chat_data['form_order_type'] = value
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    msg = update.effective_message.reply_text('Назовите озвученные цены.')
    context.chat_data['message_to_delete'] = msg.message_id
    update.effective_message.delete()
    return 'state_askform_announced_amounts'


def ask_orderform_announced_amounts(update, context):
    try:
        text = update.effective_message.text
        context.chat_data['form_order_announced_amounts'] = text
        update.effective_message.delete()
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
        delete_message_to_delete(update, context)
        msg = update.effective_message.reply_text(
            'Перечислите ВМ, которым отправить заказ. (Через запятую, с пробелами)')
        context.chat_data['message_to_delete'] = msg.message_id
    except Exception as e:
        print(e)
    return 'state_askform_masters'


def set_orderform_city(update, context, value):
    try:
        city = models.City.objects.filter(id=value).first()
        context.chat_data['form_client_city'] = city.title
        try:
            updater.bot.editMessageText(
                insert_create_order_form(updater, context),
                reply_markup=keyboards.get_create_order_keyboard(),
                chat_id=update.effective_chat.id,
                message_id=get_chat_data_or_none(context,
                                                 'order_creation_message_id'),
                parse_mode='html')
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    msg = update.effective_message.reply_text('Укажите адрес клиента')
    context.chat_data['message_to_delete'] = msg.message_id
    update.effective_message.delete()
    return 'state_askform_adress'


conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(user_response_handler)],
    states={
        'ask_order_amount': [
            MessageHandler(Filters.regex('^[0-9]+$'), ask_order_amount)],
        'ask_order_comment': [MessageHandler(Filters.text, ask_order_comment)],
        'state_askform_clientname': [
            MessageHandler(Filters.text, ask_orderform_clientname)],
        'state_askform_advertname': [
            MessageHandler(Filters.text, ask_orderform_advertname)],
        'state_askform_adress': [
            MessageHandler(Filters.text, ask_orderform_adress)],
        'state_askform_phone': [
            MessageHandler(Filters.text, ask_orderform_phone)],
        'state_askform_city': [CallbackQueryHandler(user_response_handler)],
        'state_askform_type': [CallbackQueryHandler(user_response_handler)],
        'state_askform_announced_amounts': [
            MessageHandler(Filters.text, ask_orderform_announced_amounts)],
        'state_askform_comment': [
            MessageHandler(Filters.text, ask_orderform_comment)],
        'state_askform_masters': [
            MessageHandler(Filters.text, ask_orderform_masters)],
    },
    fallbacks=[CallbackQueryHandler(user_response_handler)],
)

dispatcher.add_handler(CommandHandler('start', cmd_start))
dispatcher.add_handler(conversation)
dispatcher.add_handler(MessageHandler(Filters.text, user_response_handler))

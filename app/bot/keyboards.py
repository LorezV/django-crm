from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app import models

keyboard_profile_check = [
    [InlineKeyboardButton('Проверить статус заявки 🔄',
                          callback_data='button_update')],
    []
]

keyboard_order_manage = [
    [InlineKeyboardButton('Сумма 💸', callback_data='order_button_amount'),],
    [InlineKeyboardButton('Коммент 💬', callback_data='order_button_comment'),],
    [InlineKeyboardButton('Закрыть ✅', callback_data='order_button_close'),],
    [InlineKeyboardButton('Модерн 🔧', callback_data='order_button_modern')],
    [InlineKeyboardButton('Отменить ❌', callback_data='order_button_cancel'),],
    [InlineKeyboardButton('🔄', callback_data='order_button_update'),],
    [InlineKeyboardButton('Назад', callback_data='open_order_tabs_layout'),],
]

keyboard_order_tabs = [
    [InlineKeyboardButton(
        'Управление ⚙', callback_data='open_order_manage_layout')],
    [InlineKeyboardButton('🔄', callback_data='order_button_update')],
    [InlineKeyboardButton('➖', callback_data='hide_message')]
]


def get_create_order_keyboard():
    keyboard = []
    keyboard.append([
        InlineKeyboardButton('Изменить 🔧', callback_data='orderform_editform'),
    ])
    keyboard.append([
        InlineKeyboardButton('Создать ✔', callback_data='orderform_submit'),
    ])
    keyboard.append([
        InlineKeyboardButton('➖', callback_data='hide_message'),
    ])
    return InlineKeyboardMarkup(keyboard)


def get_profile_keyboard(profile):
    keyboard = []
    keyboard.append([InlineKeyboardButton('Мои заказы 🧐', callback_data='button_myorders'), InlineKeyboardButton(
        'Обновить данные 🔄', callback_data='button_update')])
    if profile.is_operator:
        keyboard.append([InlineKeyboardButton(
            'Создать заказ ➕', callback_data='create_order')])
    return InlineKeyboardMarkup(keyboard)


def get_order_type_keyboard(choices):
    keyboard = []
    for status in choices:
        keyboard.append([InlineKeyboardButton(
            status[1], callback_data=f'type-button_{status[0]}')])
    return InlineKeyboardMarkup(keyboard)


def get_offer_order_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Принять', callback_data='offer_accept'),
            InlineKeyboardButton('Отклонить', callback_data='hide_message'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_order_city_keyboard():
    keyboard = []
    for city in models.City.objects.all():
        keyboard.append([
            InlineKeyboardButton(
                city.title, callback_data=f'set-city_{city.id}')
        ])
    return InlineKeyboardMarkup(keyboard)

from telebot import types
import db_reserve


def kb_person():
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('На двоих', callback_data=f'two'))
    all_buttons.add(types.InlineKeyboardButton('До четверых', callback_data='four'))
    all_buttons.add(types.InlineKeyboardButton('До восьми', callback_data='up_to_eight'))
    all_buttons.add(types.InlineKeyboardButton('Больше восьми', callback_data='more_that_eight'))
    all_buttons.add(types.InlineKeyboardButton('Вернуться в главное меню', callback_data='start'))
    return all_buttons


def kb_take_table_for_person(person):
    con = db_reserve.Connect()
    button_list = con.take_table_with_person(person=person)
    all_buttons = types.InlineKeyboardMarkup()
    for table in button_list:
        all_buttons.add(types.InlineKeyboardButton(f'Номер столика: {table[0]}', callback_data=f'table*{table[0]}'))
    all_buttons.add(types.InlineKeyboardButton(f'Назад', callback_data='reserve'))
    all_buttons.add(types.InlineKeyboardButton(f'Вернуться в главное меню', callback_data='start'))
    return all_buttons


def admin_reserve(number, user_id):
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton(f'Подтвердить бронь', callback_data=f'confirmed*{number}*{user_id}'))
    all_buttons.add(types.InlineKeyboardButton(f'Отменить бронь', callback_data=f'cancellation*{number}*{user_id}'))
    return all_buttons


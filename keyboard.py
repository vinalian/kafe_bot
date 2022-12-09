from telebot import types
import db_connect


#Стартовая клавиатура
def start_menu():
    con = db_connect.Connect()
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('Посмотреть меню', callback_data=f'main_menu'))
    all_buttons.add(types.InlineKeyboardButton('Забронировать столик', callback_data='reserve'))
    return all_buttons


#Вывод категорий блюд
def kb_main_menu():
    con = db_connect.Connect()
    button_list = con.main_menu()
    all_buttons = types.InlineKeyboardMarkup()
    for title in button_list:
        all_buttons.add(types.InlineKeyboardButton(title[1], callback_data=f'menu*{title[0]}'))
    all_buttons.add(types.InlineKeyboardButton('На главную', callback_data=f'start'))
    return all_buttons


#Вывод блюд из выбранной категории
def kb_menu(menu_cat):
    con = db_connect.Connect()
    button_list = con.menu(menu_cat=menu_cat)
    all_buttons = types.InlineKeyboardMarkup()
    for title in button_list:
        all_buttons.add(types.InlineKeyboardButton(title[1], callback_data=f'item_menu*{title[0]}'))
    all_buttons.add(types.InlineKeyboardButton('Меню', callback_data=f'back_main'))
    return all_buttons


#Кнопки "Назад" и "Меню" из подгоброй информации о блюде
def kb_item(cat_name):
    con = db_connect.Connect()
    menu_cat = con.get_cut_id_byName(cat_name=cat_name)
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data=f'back_item*{menu_cat[0][0]}'))
    all_buttons.add(types.InlineKeyboardButton('Меню', callback_data=f'back_main'))
    return all_buttons


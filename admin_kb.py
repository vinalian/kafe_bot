from telebot import types
import db_connect


#Клавиатура админ панели "отказ доступа"
def not_superuser():
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('Вернуться на главную', callback_data='start'))
    return all_buttons

#Квалиатура админ панели "Стартовая панель"
def admin_kb():
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('Работа с меню', callback_data='admin_menu'))
    all_buttons.add(types.InlineKeyboardButton('Работа с логами', callback_data='admin_log'))
    all_buttons.add(types.InlineKeyboardButton('Работа с пользователями', callback_data='admin_users'))
    all_buttons.add(types.InlineKeyboardButton('Выход из админ-меню', callback_data='start'))
    return all_buttons

##Квалиатуры админ панели "ADMIN-MENU"
#Главная клавиатура
def admin_kb_menu():
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('Создать новую категорию блюд', callback_data='new_cat'))
    all_buttons.add(types.InlineKeyboardButton('Добавить новое блюдо', callback_data='new_dish'))
    all_buttons.add(types.InlineKeyboardButton('Удалить блюдо', callback_data='del_dish'))
    all_buttons.add(types.InlineKeyboardButton('Удалить категорию', callback_data='del_cat'))
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data='admin_back'))
    return all_buttons

#Квалиатура выбора для удалени категории
def admin_kb_delete_cat():
    con = db_connect.Connect()
    button_list = con.main_menu()
    all_buttons = types.InlineKeyboardMarkup()
    for title in button_list:
        all_buttons.add(types.InlineKeyboardButton(title[1], callback_data=f'delete_cat*{title[0]}'))
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data='admin_back'))
    return all_buttons

#Клавиатура выбора категории(Для удаления блюда)
def admin_kb_select_cat():
    con = db_connect.Connect()
    button_list = con.main_menu()
    all_buttons = types.InlineKeyboardMarkup()
    for title in button_list:
        all_buttons.add(types.InlineKeyboardButton(title[1], callback_data=f'select_dish*{title[0]}'))
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data='admin_back'))
    return all_buttons

#Клавиатура выбора блюда
def admin_kb_select_dish(menu_cat_id):
    con = db_connect.Connect()
    button_list = con.menu(menu_cat=menu_cat_id)
    all_buttons = types.InlineKeyboardMarkup()
    for title in button_list:
        all_buttons.add(types.InlineKeyboardButton(title[1], callback_data=f'item_menu_delete*{title[0]}'))
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data=f'admin_back'))
    return all_buttons


#Клавиатура выбота категории (для бодавлению блюда)
def admin_kb_select_cat_to_UPdate():
    con = db_connect.Connect()
    button_list = con.main_menu()
    all_buttons = types.InlineKeyboardMarkup()
    for title in button_list:
        all_buttons.add(types.InlineKeyboardButton(title[1], callback_data=f'select_dish_toUP*{title[0]}'))
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data='admin_back'))
    return all_buttons


## Главная квалиатура админ панели "ADMIN-LOG"
def admin_kb_log():
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('Топ пользователей', callback_data='users_top'))
    all_buttons.add(types.InlineKeyboardButton('Топ кнопок', callback_data='buttons_top'))
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data='admin_back'))
    return all_buttons


def admin_back_to_log():
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data='admin_log'))
    return all_buttons


#Квалиатура админ панели "ADMIN-USER"
def admin_kb_users():
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('Выдать права суперпользователя', callback_data='give_superuser'))
    all_buttons.add(types.InlineKeyboardButton('Снять права суперпользователя', callback_data='delete_superuser'))
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data='admin_back'))
    return all_buttons


#Кнопка назад в "ADMIN-MENU"
def admin_kb_btn_back():
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('Назад', callback_data='admin_back'))
    return all_buttons



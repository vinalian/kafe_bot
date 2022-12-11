from telebot import types
import db_connect
from keyboard import start_menu, kb_main_menu, kb_menu, kb_item
from loader import bot


# Команда '/start' + регистрация пользователя
@bot.message_handler(commands=['start'])
def start(message):
    con = db_connect.Connect()
    try:
        con.register_new_user(user_id=message.from_user.id, user_name=message.from_user.username)
    except:
        pass
    bot.send_message(
        message.chat.id,
        text=f'Привет {message.from_user.username}\n Что хочешь посмотреть?', reply_markup=start_menu())


# Обработчик выхода "На главную станицу"
@bot.callback_query_handler(lambda call: True if call.data == 'start' else False)
def start_button(call: types.CallbackQuery):
    bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )
    bot.send_message(
        chat_id=call.from_user.id,
        text=f'Закажем столик?',
        reply_markup=start_menu()
    )


# Вывод главного меню
@bot.callback_query_handler(
    lambda call: True if call.data.split('*')[0] == 'main_menu' or call.data.split('*')[0] == 'back_main' else False)
def main_menu(call: types.CallbackQuery):
    bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )
    bot.send_message(
        chat_id=call.from_user.id,
        text="Наше меню:",
        reply_markup=kb_main_menu()
    )


# Вывод меню блюд
@bot.callback_query_handler(
    lambda call: True if call.data.split('*')[0] == 'menu' or call.data.split('*')[0] == 'back_item' else False)
def menu(call: types.CallbackQuery):
    con = db_connect.Connect()
    cat_name = con.get_dish_name_byID(id=int(call.data.split('*')[1]))[0][0]
    bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )
    bot.send_message(
        chat_id=call.from_user.id,
        text=f"Блюда категории {cat_name}",
        reply_markup=kb_menu(menu_cat=int(call.data.split('*')[1]))
    )


# Вывод информации о блюде
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0] == 'item_menu' else False)
def item_info(call: types.CallbackQuery):
    con = db_connect.Connect()
    info = con.get_item_info(id=call.data.split('*')[1])[0]
    bot.send_photo(
        chat_id=call.from_user.id,
        photo=info[4],
        caption = f"{info[0]}\n Цена: {info[1]} Byn \n Вес: {info[2]} грамм "
           f"\n Описание: {info[3]}",
        reply_markup = kb_item(cat_name=info[0])
    )
    bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )











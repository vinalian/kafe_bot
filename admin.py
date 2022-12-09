from telebot import types
import db_admin
import admin_kb
import db_log
from admin_kb import admin_kb_menu, admin_kb_log, admin_kb_users, admin_kb, not_superuser, admin_kb_btn_back, \
    admin_kb_delete_cat, admin_kb_select_cat, admin_kb_select_dish, admin_kb_select_cat_to_UPdate, \
    admin_kb_btn_close
from loader import bot


# Админ панель
@bot.message_handler(commands=['admin'])
def admin_first(message):
    try:
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id,
        )
    except:
        pass
    try:
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id - 1,
        )
    except:
        pass
    con = db_admin.Connect_menu()
    is_superuser = con.if_superuser(user_id = message.from_user.id)
    if is_superuser[0] == '1' or is_superuser[0] == 1:
        bot.send_message(
            message.chat.id,
            text=f'Доступ получен!\n Добрый день {message.from_user.first_name}',
            reply_markup=admin_kb()
        )
    else:
        bot.send_message(
            message.chat.id,
            text='У вас не достаточно прав!',
            reply_markup=not_superuser()
        )


@bot.callback_query_handler(lambda call: True if call.data == 'admin_back' else False)
def admin_back_btn(call:types.CallbackQuery):
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f'Доступ получен!\n Добрый день {call.from_user.username}',
        reply_markup=admin_kb()
    )


@bot.callback_query_handler(lambda call: True if call.data == 'admin_menu' or
                                                 call.data == 'admin_log' or
                                                 call.data == 'admin_users'
                                                                         else False)
def admin_menu(call:types.CallbackQuery):
    match call.data:
        case 'admin_menu':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Вы вошли в редактор меню",
                reply_markup=admin_kb_menu()
            )

        case 'admin_log':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Вы вошли в меню лучших пользователей",
                reply_markup=admin_kb_log()
            )
        case 'admin_users':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Вы вошли в меню прав суперпользователя",
                reply_markup=admin_kb_users()
            )


##Админ-меню.
#Match_case
@bot.callback_query_handler(lambda call: True if call.data == 'new_cat' or
                                                 call.data == 'new_dish' or
                                                 call.data == 'del_dish' or
                                                 call.data == 'del_cat'
                                                                       else False)
def admin_change_menu(call:types.CallbackQuery):
    match call.data:
        case 'new_cat':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Введите название новой категории. Для отмены нажмите 'BACK' ",
                reply_markup=admin_kb_btn_back()
            )
            bot.register_next_step_handler(call.message, new_cat)

        case 'del_cat':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Выберите категорию для удаления. Для отмены нажмите 'BACK' ",
                reply_markup=admin_kb_delete_cat()
            )

        case 'del_dish':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Выберите категорию для удаления блюда. Для отмены нажмите 'BACK' ",
                reply_markup=admin_kb_select_cat()
            )

        case 'new_dish':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Выберите категорию для добавления блюда и её описание через запятую. Для отмены нажмите 'BACK' ",
                reply_markup=admin_kb_select_cat_to_UPdate()
            )

#Добавление новой категории блюд
def new_cat(message):
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id - 1,
    )
    try:
        cat_name = message.text.split(',')[0]
        disc = message.text.split(',')[1]
        con = db_admin.Connect_menu()
        add_cat = con.create_new_cat(cat_name=cat_name, disc=disc)
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Добавлена новая категория:  {cat_name}\n Описание: {disc}',
            reply_markup=admin_kb_btn_back()
        )

    except:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Произошла ошибка. Выберите другое название категории!',
            reply_markup=admin_kb_btn_back()
        )

#Добавление нового блюда. Выбор категории для нового блюда
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0] == 'select_dish_toUP' else False)
def new_dish(call:types.CallbackQuery):
    cat_id = call.data.split('*')[1]
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f"Отправьте фото блюдо с название, ценой, весом и описанием (через запятую)"
             f"\n Для отмены нажмите 'BACK' ",
        reply_markup=admin_kb_btn_back()
    )
    bot.register_next_step_handler(call.message, new_dish_info, cat_id)

#Добавление нового блюда. Получение описания нового блюда.
def new_dish_info(message, cat_id):
    con = db_admin.Connect_menu()
    con.add_new_dish(dish = message.caption.split(',')[0],
                     price=message.caption.split(',')[1],
                     weight=message.caption.split(',')[2],
                     desc=message.caption.split(',')[3],
                     image_id=message.photo[0].file_id,
                     cat_id=cat_id
    )
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id-1,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Добавлено новое блюдо:  {message.caption.split(',')[0]}",
        reply_markup=admin_kb_btn_back()
    )

#Удаление категории блюд.
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0] == 'delete_cat' else False)
def delete_cat(call:types.CallbackQuery):
    con = db_admin.Connect_menu()
    con.delete_cat(cat_id=call.data.split('*')[1])
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f"Вы успешно удалили категорию",
        reply_markup=admin_kb_btn_back()
    )

#Удаление блюда. Выбор категории удаляемого блюда.
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0] == 'select_dish' else False)
def select_cat_to_delete(call:types.CallbackQuery):
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f"Выберите блюдо для удаления",
        reply_markup=admin_kb_select_dish(menu_cat_id=call.data.split('*')[1])
    )

#Удаление блюда. Выбор удаляемого блюда.
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0] == 'item_menu_delete' else False)
def delete_dish(call:types.CallbackQuery):
    con = db_admin.Connect_menu()
    con.delete_dish(dish_id=call.data.split('*')[1])
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f"Блюдо было удалено!",
        reply_markup=admin_kb_btn_back()
    )

#Топ пользователей
@bot.callback_query_handler(lambda call: True if call.data == 'users_top' else False)
def users_top(call:types.CallbackQuery):
    con = db_admin.Connect_log()
    top_users = con.get_users_top()
    user_1 = con.get_user_name_byID(user_id=top_users[0][0])
    user_2 = con.get_user_name_byID(user_id=top_users[1][0])
    user_3 = con.get_user_name_byID(user_id=top_users[2][0])
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f'🥇   {user_1[0]}    Нажатий: {top_users[0][1]}\n'
             f'🥈   {user_2[0]}    Нажатий: {top_users[1][1]}\n'
             f'🥉   {user_3[0]}    Нажатий: {top_users[2][1]}\n',
        reply_markup=admin_kb_btn_back()
    )

#Топ кнопок
@bot.callback_query_handler(lambda call: True if call.data == 'buttons_top' else False)
def admin_buttons_top(call:types.CallbackQuery):
    con = db_admin.Connect_log()
    top_buttons = con.get_buttons_top()
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f'Топ нажатых кнопок за неделю: \n'
             f'🥇   {top_buttons[0][0]}\n                      Нажатий: {top_buttons[0][1]}\n'
             f'🥈   {top_buttons[1][0]}\n                      Нажатий: {top_buttons[1][1]}\n'
             f'🥉   {top_buttons[2][0]}\n                      Нажатий: {top_buttons[2][1]}\n'
             f'4   {top_buttons[3][0]}\n                       Нажатий: {top_buttons[3][1]}\n'
             f'5   {top_buttons[4][0]}\n                       Нажатий: {top_buttons[4][1]}\n',
        reply_markup=admin_kb_btn_back()
    )

#Запрос ввода имени нового админа
@bot.callback_query_handler(lambda call: True if call.data == 'give_superuser' else False)
def select_user_to_give_superuser(call:types.CallbackQuery):
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text='Введите USERNAME пользователя для выдачи прав администратора',
        reply_markup=admin_kb_btn_back()
    )
    bot.register_next_step_handler(call.message, give_superuser)

#Добавление нового админа
def give_superuser(message):
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id - 1,
    )
    try:
        con = db_admin.Connect_superuser()
        con.give_superuser(user_name=message.text)
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Добавлен новый администратор:  {message.text}',
            reply_markup=admin_kb_btn_back()
        )
    except:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Ошибка добавления администратора',
            reply_markup=admin_kb_btn_back()
        )

#Запрос выбора админа для удаления
@bot.callback_query_handler(lambda call: True if call.data == 'delete_superuser' else False)
def select_user_to_give_superuser(call:types.CallbackQuery):
    con = db_admin.Connect_superuser()
    take_all_superuser = con.select_all_superuser()
    all_superuser = types.InlineKeyboardMarkup()
    for title in take_all_superuser:
        all_superuser.add(types.InlineKeyboardButton(title[0], callback_data=f'superuser*{title[0]}'))
    all_superuser.add(types.InlineKeyboardButton('Назад', callback_data='admin_back'))
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text='Выберите администратора для удаления прав',
        reply_markup=all_superuser
    )
    bot.register_next_step_handler(call.message, give_superuser)

#Удаление админа
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0] == 'superuser' else False)
def delete_superuser(call:types.CallbackQuery):
    con = db_admin.Connect_superuser()
    con.del_superuser(user_name=call.data.split('*')[1])
    print(call.data.split('*')[1])
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f"Вы удалили администратора {call.data.split('*')[1]}",
        reply_markup=admin_kb_btn_back()
    )

#Выгрузка логов из БД
@bot.callback_query_handler(lambda call: True if call.data == 'get_logs' else False)
def get_logs(call:types.CallbackQuery):
    con = db_admin.Connect_log()
    take_logs = con.take_logs()
    logs = ''
    for log in take_logs:
        logs += f'{log}\n'
    log_file = open("Logs", "w", encoding='utf8')
    log_file.write(logs)
    log_file.close()
    bot.send_document(
        chat_id=call.from_user.id,
        document=types.InputFile('Logs'),
        caption=f"Выгруженные логи:",
        reply_markup=admin_kb_btn_close()
    )

@bot.callback_query_handler(lambda call: True if call.data == 'close' else False)
def close(call:types.CallbackQuery):
    bot.delete_message(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
    )
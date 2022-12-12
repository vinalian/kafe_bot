import telebot
import db_log


telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot('5929731710:AAHnjp7TSOivtslH7sAdefdONdJsjPEk9aY')


@bot.middleware_handler()
def middleware_handler(bot_instance, package):
    if package.message != None:
        user_id = package.message.from_user.id
        message = package.message.text
        con = db_log.Connect()
        con.log(user_id=user_id, button=message)
    else:
        user_id = package.callback_query.from_user.id
        callback_data = package.callback_query.data
        match callback_data.split('*')[0]:
            case 'start':
                try:
                    con = db_log.Connect()
                    con.log(button="На главную", user_id=user_id)
                except Exception as error:
                    print(error)

            case 'main_menu':
                try:
                    con = db_log.Connect()
                    con.log(button="Посмотреть меню", user_id=user_id)
                except Exception as error:
                    print(error)

            case 'reserve':
                try:
                    con =db_log.Connect()
                    con.log(button="Забронировать столик", user_id=user_id)
                except Exception as error:
                    print(error)

            case 'menu':
                try:
                    con = db_log.Connect()
                    button_name = con.get_menu_name_for_id(id=package.callback_query.data.split('*')[1])
                    con.log(button=button_name[0], user_id=user_id)
                    con.log_buttons(button_name=button_name[0], user_id=user_id)
                except Exception as error:
                    print(error)

            case 'back_item':
                try:
                    con = db_log.Connect()
                    con.log(button="Назад", user_id=user_id)
                except Exception as error:
                    print(error)

            case 'back_main':
                try:
                    con = db_log.Connect()
                    con.log(button="Меню", user_id=user_id)
                except Exception as error:
                    print(error)

            case 'item_menu':
                try:
                    con = db_log.Connect()
                    button_name = con.get_dish_name_for_id(id=package.callback_query.data.split('*')[1])
                    con.log(button=button_name[0], user_id=user_id)
                    con.log_buttons(button_name=button_name[0], user_id=user_id)
                except Exception as error:
                    print(error)

            case 'table':
                try:
                    con = db_log.Connect()
                    con.log(button=f"Бронь столика № {package.callback_query.data.split('*')[1]}", user_id=user_id)
                except Exception as error:
                    print(error)

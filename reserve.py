from telebot import types
from keyboard import start_menu
from loader import bot
import db_reserve
from reserve_kb import kb_person, kb_take_table_for_person, kb_reserve_main_menu
from admin_kb import admin_reserve



@bot.callback_query_handler(lambda call: True if call.data.split('*')[0] == 'reserve' else False)
def reserve(call: types.CallbackQuery):
    bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )
    bot.send_message(
        chat_id=call.from_user.id,
        text=f"На какое количество человек нужен столик?",
        reply_markup=kb_person()
    )


@bot.callback_query_handler(lambda call: True if
                                                call.data == 'two' or
                                                call.data == 'four' or
                                                call.data == 'up_to_eight' or
                                                call.data == 'more_that_eight'
                                                                                else False)
def reserve(call:types.CallbackQuery):
    match call.data:
        case 'two':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Свободные столики на двоих",
                reply_markup=kb_take_table_for_person(person=2)
            )
        case 'four':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Свободные столики до четверых человек",
                reply_markup=kb_take_table_for_person(person=4)
            )
        case 'up_to_eight':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Свободные столики до восьми человек",
                reply_markup=kb_take_table_for_person(person=8)
            )
        case 'more_that_eight':
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Для бронирования столиков на большое количество человек свяжитесь с администратором по номеру: \n"
                     f"+375(29)111-11-11'",
                reply_markup=kb_take_table_for_person(person=10)
            )


@bot.callback_query_handler(lambda call: True if call.data.split('*')[0] == 'table' else False)
def is_reserved(call:types.CallbackQuery):
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f"Заявка на бронь столика №{call.data.split('*')[1]} отправлена.",
        reply_markup=kb_reserve_main_menu()
    )
    bot.send_message(
        chat_id=1896234699,
        text=f"@{call.from_user.username} хочет забронировать столик №{call.data.split('*')[1]}",
        reply_markup=admin_reserve(number=call.data.split('*')[1], user_id=call.from_user.id)
    )



@bot.callback_query_handler(lambda call: True if
                                                call.data.split('*')[0] == 'confirmed' or
                                                call.data.split('*')[0] == 'cancellation'
                                                                                            else False)
def confirmed(call:types.CallbackQuery):
    match call.data.split('*')[0]:
        case 'confirmed':
            con = db_reserve.Connect()
            con.confirmed_reserve(table_number=call.data.split('*')[1])
            bot.send_message(
                chat_id = call.data.split('*')[2],
                text=f"Ваша бронь столика № {call.data.split('*')[1]} подтверждена!"
            )
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Бронь столика №{call.data.split('*')[1]} подтверждена"
            )
        case 'cancellation':
            bot.send_message(
                chat_id = call.data.split('*')[2],
                text=f"Ваша бронь столика № {call.data.split('*')[1]} отменена!"
            )
            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f"Бронь столика №{call.data.split('*')[1]} отменена"
            )


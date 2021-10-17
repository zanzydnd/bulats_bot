import re

import telebot
from telebot import types

data_user = []


def valid_email(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


def valid_vk(vk):
    return bool(re.search(r"vk.com\/\w+", vk))


def manager(message, client):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_meneger = types.KeyboardButton(text="/Менеджер")
    keyboard.add(button_meneger)
    client.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)

    @client.message_handler(commands=['Менеджер'])
    def message_to_choose_what_have_been_sold(message):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Математика', callback_data='Математика'))
        markup.add(telebot.types.InlineKeyboardButton(text='Информатика', callback_data='Информатика'))
        markup.add(telebot.types.InlineKeyboardButton(text='Обществознание', callback_data='Обществознание'))
        client.send_message(message.chat.id, text="Выбери предмет!", reply_markup=markup)

    @client.callback_query_handler(
        func=lambda call: call.data and call.data != "Верно" and call.data != "Отредактировать")
    def handle_chosen_subject(call):
        client.send_message(call.message.chat.id, text="Выбери тариф!")
        keyboard_tarif = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        # TODO: вытягивание тарифов.
        # get_all_tarifes_avalible
        button_vip = types.KeyboardButton(text="VIP")
        button_standart = types.KeyboardButton(text="Standart")
        keyboard_tarif.add(button_vip, button_standart)
        send = client.send_message(call.message.chat.id, 'Тарифы', reply_markup=keyboard_tarif)
        client.register_next_step_handler(send, handle_chosen_tarif, subject_name=call.data)

    def handle_chosen_tarif(message, subject_name):
        print(subject_name)
        # TODO: переделать на класс Tarif
        data_user.clear()
        data_user.append(subject_name)
        data_user.append(message.text)
        send = client.send_message(message.chat.id, 'Теперь введи данные ученика!')
        client.register_next_step_handler(send, handle_student_info, subject_tarif=[subject_name, message.text])

    def handle_student_info(message, subject_tarif):
        dan = message.text.split('\n')
        if len(dan) == 3:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Верно', callback_data='Верно'))
            markup.add(telebot.types.InlineKeyboardButton(text='Отредактировать', callback_data='Отредактировать'))
            if valid_email(dan[2].strip()) == True and valid_vk(dan[1].strip()) == True:
                client.send_message(message.chat.id,
                                    'Проверь данные!' + '\n' + 'Предмет: ' + subject_tarif[0] + '\n' + 'Тариф: ' +
                                    subject_tarif[1] + '\n' + 'Ф.И.О: ' + dan[0] + '\n' + 'VK: ' + dan[
                                        1] + '\n' + 'Email: ' +
                                    dan[2], reply_markup=markup)
            else:
                send = client.send_message(message.chat.id,
                                           'Проверь данные email или vk и отправь мне данные заново')
                client.register_next_step_handler(send, handle_student_info, subject_tarif=subject_tarif)
        else:
            send = client.send_message(message.chat.id, "Введено не правильно, отправь заново данные")
            client.register_next_step_handler(send, handle_student_info, subject_tarif=subject_tarif)

    @client.callback_query_handler(func=lambda call: call.data == 'Отредактировать')
    def query_handler_redaktirovat(call):
        send = client.send_message(call.message.chat.id, text="Отправь данные ученика заново!")
        client.register_next_step_handler(send, handle_student_info)

    @client.callback_query_handler(func=lambda call: call.data == 'Верно')
    def query_handler_verno(call):
        keyboard1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_meneger_z = types.KeyboardButton(text="/Менеджер")
        keyboard1.add(button_meneger_z)
        client.send_message(call.message.chat.id, text="Успешно добавлена в бд, сейчас будет отправлена куратору!",
                            reply_markup=keyboard1)
        if data_user[0] == 'Математика':
            client.send_message('394239293',
                                text='У тебя новый ученик! Скорее поприветствуй его ' + '\n' + data_user[2])
            # Курсор для выполнения операций с базой данных
            # cursor1 = connection.cursor()
            # Добавление в базу данных math_id
            # postgres_insert_math_id1 = '''INSERT INTO math_id (Name_predmet, Tarif, DannieUchenika, URL_vk, Email) VALUES (%s,%s,%s,%s,%s)'''
            # record_to_insert_math_id1 = (temp_d[0], temp_d[1], temp_d[2], temp_d[3], temp_d[4])
            # Выполнение SQL-запроса
            # cursor1.execute(postgres_insert_math_id1, record_to_insert_math_id1)
            # connection.commit()
            # count1 = cursor1.rowcount
        # print(count1, "Запись успешно добавлена в таблицу mobile")
        # temp_d.clear()

        # elif data_user[0] == 'Информатика':
        # temp = ['Predmet', 'Tarif', 'F.I.O', 'Vk', 'Email']
        #    bot.send_message('856379026',
        #                     text='У тебя новый ученик! Скорее поприветствуй его ' + '\n' + data_user[2])
        # Курсор для выполнения операций с базой данных
        # cursor = connection.cursor()
        # Добавление в базу данных math_id
        #    print(temp_d['Predmet'])
        # postgres_insert_math_id = '''INSERT INTO math_id (Name_predmet, Tarif, DannieUchenika, URL_vk, Email) VALUES (%s,%s,%s,%s,%s)'''
        # record_to_insert_math_id = (temp_d['Predmet'], temp_d['Tarif'], temp_d['F.I.O'], temp_d['Vk'], temp_d['Email'])
        # Выполнение SQL-запроса
        # cursor.execute(postgres_insert_math_id,record_to_insert_math_id)
        # connection.commit()
        # count = cursor.rowcount
        # print (count, "Запись успешно добавлена в таблицу mobile")

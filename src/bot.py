import re

import telebot
from telebot import types

import conf
from curators_logic import curator
from manager_logic import manager

client = telebot.TeleBot(conf.TOKEN)

manager_bool = True
curator_boolean = True
data_user = []


@client.message_handler(commands=['start'])
def main(message):
    # TODO: менеджеры
    if manager_bool:
        manager(message, client)
    # TODO: кураторы
    elif curator_boolean:
        curator(message, client)

client.polling()
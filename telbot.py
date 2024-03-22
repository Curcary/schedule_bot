# -*- coding: utf-8 -*-
import telebot as tb
import parsing as p
import pickle
from telebot import types
from secret import *

DATAFILE = 'data/user_id.dat'

bot = tb.TeleBot(TOKEN)


def send_schedule(id, text):
    lessons = parser.parse(text)
    bot.send_message(id, lessons)


def update():
    with open(DATAFILE, 'rb') as file:
        chat_ids = pickle.load(file)
        for id in chat_ids:
            bot.send_message(id, "Расписание обновлено")


parser = p.parser(update)

LIST_OF_GROUPS = parser.get_groups()


@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btnUpdates = types.InlineKeyboardButton('Получать обновления', callback_data='updates')
    markup.row(btnUpdates)
    bot.send_message(message.from_user.id, 'Введите номер группы без точки, начиная с "/"\nНапример /1202')
    bot.send_message(message.from_user.id, 'Чтобы посмотреть список групп, напишите /группы', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def get_updates(callback):
    if callback.data == 'updates':
        with open(DATAFILE, 'rb') as file:
            chat_ids = pickle.load(file)
            chat_ids.add(callback.message.chat.id)
        with open(DATAFILE, 'wb') as file:
            pickle.dump(chat_ids, file)
        bot.send_message(callback.message.chat.id, 'Вы будете получать уведомления об обновлении\n')
        bot.send_message(callback.message.chat.id, 'Чтобы отказаться от обновлений, напишите /отмена\n')


@bot.message_handler(commands=LIST_OF_GROUPS)
def select_group_handler(message: types.Message):
    send_schedule(message.from_user.id, message.text[1:])


@bot.message_handler(commands=['отмена'])
def decline_updates(message: types.Message):
    with open(DATAFILE, 'rb') as file:
        chat_ids = pickle.load(file)
        chat_ids.discard(message.chat.id)
    with open(DATAFILE, 'wb') as file:
        pickle.dump(chat_ids, file)
    bot.send_message(message.chat.id, "Вы отписались от уведомлений")


@bot.message_handler(commands=['группы'])
def groups(message: types.Message):
    outmessage = ''
    for l in range(0, len(LIST_OF_GROUPS), 2):
        outmessage += '/' + LIST_OF_GROUPS[l] + '\t /' + LIST_OF_GROUPS[l + 1] + "\n"
    bot.send_message(message.from_user.id, outmessage)


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except ConnectionError:
        pass

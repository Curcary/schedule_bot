import telebot as tb
import parsing as p
import pickle
from telebot import types

TOKEN = ""

DATAFILE = 'data/user_id.dat'

bot = tb.TeleBot(TOKEN)
LIST_OF_GROUPS = ['1121','0921','0922','1221', '1222', '1521', 
'2321', '0911','0912','1111','1102', '1101', '1191', '1192', 
'1211', '1212', '1213', '1202', '1201', '1291', '1292', '1511',
 '1501', '1591','1581', '2311', '2301', '2391']


def update():
    with open(DATAFILE, 'rb') as file:
        chat_ids = pickle.load(file)
        for id in chat_ids:
            bot.send_message(id, "Расписание обновлено")

@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btnUpdates = types.InlineKeyboardButton('Получать обновления', callback_data='updates')
    markup.row(btnUpdates)
    bot.send_message(message.from_user.id,'Введите номер группы без точки, начиная с "/"\nНапример /1202')
    bot.send_message(message.from_user.id,'Чтобы посмотреть список групп, напишите /группы', reply_markup= markup)

@bot.callback_query_handler(func= lambda callback: True)
def get_updates(callback):
    if callback.data == 'updates':
        with open(DATAFILE, 'rb') as file:
            chat_ids = pickle.load(file)
        with open(DATAFILE, 'wb') as file:
            chat_ids.add(callback.message.chat.id)
            pickle.dump(chat_ids, file)
        bot.send_message(callback.message.chat.id, 'Вы будете получать уведомления об обновлении\n')

@bot.message_handler(commands=LIST_OF_GROUPS)
def select_group_handler(message: types.Message):
    lessons = parser.parse(message.text[1:])
    bot.send_message(message.from_user.id, lessons)
    
@bot.message_handler(commands=['группы'])
def groups(message: types.Message):
    outmessage = ''
    for l in range(0, len(LIST_OF_GROUPS), 2):
        outmessage+='/'+ LIST_OF_GROUPS[l]+ '\t /'+ LIST_OF_GROUPS[l+1]+"\n"
    bot.send_message(message.from_user.id, outmessage)

parser = p.parser(update)
bot.polling(none_stop=True)
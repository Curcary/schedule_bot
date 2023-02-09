import parsing as p
import asyncio as a
from aiogram import Bot, Dispatcher, executor, types

TOKEN = ""
LIST_OF_GROUPS = ['1121','0921','0922','1221', '1222', '1521', 
'2321', '0911','0912','1111','1102', '1101', '1191', '1192', 
'1211', '1212', '1213', '1202', '1201', '1291', '1292', '1511',
 '1501', '1591','1581', '2311', '2301', '2391']

chat_ids = {491751773}


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


def send_update_message(loop):

    for id in chat_ids:
        bot.send_message(id, "Расписание обновлено")

def update():
    loop = a.new_event_loop()
    a.set_event_loop(loop=loop)
    loop.run_until_complete(send_update_message(loop))
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    chat_ids.add(message.from_user.id)
    print(message.from_user.id)
    await message.answer('Введите номер группы без точки, начиная с "/"\nНапример /1202')
    await message.answer('Чтобы посмотреть список групп, напишите /группы')

@dp.message_handler(commands=LIST_OF_GROUPS)
async def select_group_handler(message: types.Message):
    lessons = parser.parse(message.text[1:])
    print(message.from_user.full_name)
    await message.answer(text=lessons)
    
@dp.message_handler(commands=['группы'])
async def groups(message: types.Message):
    outmessage = ''
    for l in range(0, len(LIST_OF_GROUPS), 2):
        outmessage+='/'+ LIST_OF_GROUPS[l]+ '\t /'+ LIST_OF_GROUPS[l+1]+"\n"
    await message.answer(outmessage)

parser = p.parser(update)
executor.start_polling(dp)

import json
from aiogram import Bot, Dispatcher,executor,types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tkinter import PhotoImage


token ='5396262849:AAHfchJgx8sQHSlDWRAX7K82IWjoAPJBvXA'
bot=Bot(token=token)
dp=Dispatcher(bot)
main_content = json.load(open(r".\main_content.json"), encoding='utf-8')['contents']
lang_buttons_list=[]
lang_list=[]
home_languaged=None
##################indexing content###########################
cont=0
id_home_list=[]
id_video_list=[]
for i in main_content:
   for j in i['home']:
       j['id'] = cont
       id_home_list.append(cont)
       cont += 1
       if(j['msg_type']=="video_list"):
           for k in j['button_list']:
               k['id']=cont
               id_video_list.append(cont)
               cont+=1

#############################################################

def dispatcher(id=-1):
    for i in main_content:
        for j in i['home']:
            if(j['id']==id):
                return j
            elif(j['msg_type']=="video_list"):
                for k in j['button_list']:
                    if(k['id']==id):
                        return k




for i in main_content:
    lang=i['lang']
    lang_list.append(lang)
    lang_buttons_list.append(InlineKeyboardButton(text=lang,callback_data=lang))
keyboard_inline = InlineKeyboardMarkup().add(*lang_buttons_list)

def home_keyboard(content):
    home_button_list=[]
    for i in content:
        home_button_list.append(InlineKeyboardButton(text=i['label'],callback_data=i['id']))
    return InlineKeyboardMarkup().add(*home_button_list)
def videos_keyboard(content):
    videos_button_list=[]
    for i in content["button_list"]:
        videos_button_list.append(InlineKeyboardButton(text=i['label'],callback_data=i['id']))
    return InlineKeyboardMarkup().add(*videos_button_list)

@dp.message_handler(commands=['start','help'])
async def welcome(message: types.Message):
    await message.reply("hello",reply_markup=keyboard_inline)



@dp.message_handler(commands=['home'])
async def welcome(message: types.Message):
    await message.reply(home_languaged)




@dp.callback_query_handler(text=lang_list)
async def select_lang(call: types.CallbackQuery):
    for c in main_content:
        if c['lang'] == call.data:
           home_languaged=c['home']
           await call.message.reply(text="Home",reply_markup=home_keyboard(home_languaged))
    await call.answer()


@dp.callback_query_handler(text=id_home_list)
async def get_content(call: types.CallbackQuery):
    id=int(call.data)
    content=dispatcher(id)

    if(content["msg_type"]=="text"):
        #TODO inserire nella risposta foto se contenute
        await call.message.reply(text=content['text'])


    elif(content["msg_type"]=="video_list"):
        await call.message.reply(text="videos",reply_markup=videos_keyboard(content))

    await call.answer()

@dp.callback_query_handler(text=id_video_list)
async def get_videos(call: types.CallbackQuery):
    id = int(call.data)
    content = dispatcher(id)
    #TODO inviare video
    await call.message.reply(text="ecco il video: "+content['label'])
    await call.answer()


executor.start_polling(dp)
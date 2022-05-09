import json 

from aiogram import Bot, Dispatcher,executor,types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



token ='5396262849:AAHfchJgx8sQHSlDWRAX7K82IWjoAPJBvXA'
bot=Bot(token=token)
dp=Dispatcher(bot)
main_content = json.load(open(r".\main_content.json","rb"),)['contents']
bot.set_my_commands
print(main_content)
lang_list = []
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
print(main_content)
#############################################################
#TODO può essere migliorata
def dispatcher(id=-1):
    for i in main_content:
        for j in i['home']:
            if(j['id']==id):
                return j
            elif(j['msg_type']=="video_list"):
                for k in j['button_list']:
                    if(k['id']==id):
                        return k


def lang_keyborad(content):
    lang_buttons_list = []

    for i in content:
        lang=i['lang']
        if(lang not in lang_list):
            lang_list.append(lang)
        
        lang_buttons_list.append(InlineKeyboardButton(text=lang,callback_data=lang))
    m=InlineKeyboardMarkup(row_width=1)
    m.add(*lang_buttons_list)
    return m

def home_keyboard(content):
    home_button_list=[]
    for i in content:
        home_button_list.append(InlineKeyboardButton(text=i['label'],callback_data=i['id']))
        m=types.InlineKeyboardMarkup(row_width=1)
    
    return m.add(*home_button_list)

def videos_keyboard(content):
    videos_button_list=[]
    for i in content["button_list"]:
        videos_button_list.append(InlineKeyboardButton(text=i['label'],callback_data=i['id']))
        m=types.InlineKeyboardMarkup(row_width=1)
    return m.add(*videos_button_list)

@dp.message_handler(commands=['start','help'])

async def welcome(message: types.Message):
    id_user=message.from_user.id
    
    await bot.send_message(id_user,"hello",reply_markup=lang_keyborad(main_content))

@dp.message_handler(commands=['language'])
async def welcome(message: types.Message):
    id_user=message.from_user.id
    
    await bot.send_message(id_user,"choose:",reply_markup=lang_keyborad(main_content))

@dp.message_handler(commands=['home'])
async def welcome(message: types.Message):
    id_user=message.from_user.id
    
    await bot.send_message(id_user,home_languaged)




@dp.callback_query_handler(text=lang_list)
async def select_lang(call: types.CallbackQuery):
    id_user=call.from_user.id
    for c in main_content:
        if c['lang'] == call.data:
           home_languaged=c['home']
        
           await bot.send_message(id_user,text="Ecco la tua home",reply_markup=home_keyboard(home_languaged))
    await call.answer()


@dp.callback_query_handler(text=id_home_list)
async def get_content(call: types.CallbackQuery):
    id_user=call.from_user.id
    print(call)
    id=int(call.data)
    content=dispatcher(id)


    if(content["msg_type"]=="text"):
        #TODO inserire nella risposta foto se contenute
        
        s=content['text']
        await bot.send_message(id_user,str(s))


    elif(content["msg_type"]=="video_list"):
        
        await bot.send_message(id_user,text="videos",reply_markup=videos_keyboard(content))
    await call.answer()

@dp.callback_query_handler(text=id_video_list)
async def get_videos(call: types.CallbackQuery):
    id_user=call.from_user.id
    id = int(call.data)
    content = dispatcher(id)
    src=content['src']
    
    
    
    await bot.send_message(id_user,"ecco il video:"+content['label'])
    
    
    await bot.send_video(id_user,video=open(src,'rb'))
    await call.answer()


executor.start_polling(dp)
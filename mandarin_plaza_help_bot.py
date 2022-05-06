import json
from telegram import *
import telebot
from telebot import *
import wget


token ='1629663298:AAGIgrDZlmIyb-ORnlLm7uOiU9uYx4uGWZI'
bot = telebot.TeleBot(token)
lang=0
main_content=json.load(open(r"C:\Users\Asus\Desktop\Mandarin-plaza-help-bot\main_content.json"))
                                

# current_language="it"

# def content_languaged():
#     for c in main_content['contents']:
#         if c['lang']==current_language:
#             return c

# print(content_languaged())

def creaMark(row,s):
    l=main_content['contents'][0][s]

    ret=types.InlineKeyboardMarkup(row_width=row)
    cont=0
    for i in l :
         print(i)
         print(i['label'],i['text'])
         print(type(i['label']))
         btn=types.InlineKeyboardButton(i['label'],callback_data=i['text'])
         ret.add(btn)
         cont+=1
         
    return ret

@bot.callback_query_handler(func= lambda  call:True)
def video_callback(call): # <- passes a CallbackQuery type object to your function
    print(call)
    id=call.from_user.id
    data=call.data
    query_id=call.id
    if(data =="tutorial"):
         m=types.InlineKeyboardMarkup(row_width=1)
         l=main_content['contents'][0]['home'][2]['button_list']
         for i in l:
             btn=types.InlineKeyboardButton(i['label'],callback_data=i['src'])
             m.add(btn)
         bot.send_message(id,"tutorial:",reply_markup=m)
    bot.answer_callback_query(query_id)
    if("mp4" in data):
         bot.send_video(id,video=open(data,'rb'))
         bot.answer_callback_query(query_id)
    else:
        
        bot.send_message(id,data)
        
        bot.answer_callback_query(query_id)
    return

def main():
    markup=creaMark(1,'home')
    while(True):
        @bot.message_handler(commands=['help','start'] )
        def send_welcome(msg):

            id=msg.chat.id
            bot.send_message(id,"ciao",reply_markup=markup)
        bot.polling(none_stop=True)

main()
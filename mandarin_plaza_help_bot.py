import json
from tkinter import PhotoImage
from telegram import *
import telebot
from telebot import *
import wget



token ='1629663298:AAGIgrDZlmIyb-ORnlLm7uOiU9uYx4uGWZI'
bot = telebot.TeleBot(token)
main_content=json.load(open(r"C:\Users\Asus\Desktop\Mandarin-plaza-help-bot\main_content.json"))
naz=0


def ling():
   lingue=[]
   for c in main_content['contents']:
         if c['lang'] not in lingue:
             lingue.append(c['lang'])
   return lingue
   



def creaMark(row,s,n):
    print("naz:",n)
    naz=n
    l=main_content['contents'][naz][s]
    ret=types.InlineKeyboardMarkup(row_width=row)
    lang=types.InlineKeyboardButton("change language",callback_data="lang")
    ret.add(lang)
    
    for i in l :
         btn=types.InlineKeyboardButton(i['label'],callback_data=i['text'])
         ret.add(btn)
         
    return ret

@bot.callback_query_handler(func= lambda  call:True)
def video_callback(call): 
    lingue=ling()
    id=call.from_user.id
    data=call.data
    query_id=call.id

    if(data in lingue):
        n=lingue.index(data)
        print(n)
        m=creaMark(1,'home',n)
        bot.answer_callback_query(query_id)
        bot.send_message(id,data,reply_markup=m)


        

    elif(data=="lang"):
        m=types.InlineKeyboardMarkup(row_width=1)
        for i in lingue:
             btn=types.InlineKeyboardButton(i,callback_data=i)
             m.add(btn)
        bot.send_message(id,"language:",reply_markup=m)
        
    elif(data =="tutorial"):
         m=types.InlineKeyboardMarkup(row_width=1)
         
         l=main_content['contents'][naz]['home'][2]['button_list']
         for i in l:
             btn=types.InlineKeyboardButton(i['label'],callback_data=i['src'])
             m.add(btn)
         bot.send_message(id,"tutorial:",reply_markup=m)
         bot.answer_callback_query(query_id)

    elif("mp4" in data):
         bot.send_video(id,video=open(data,'rb'))
         bot.answer_callback_query(query_id)

    else:
        
        bot.send_message(id,data)
        
        bot.answer_callback_query(query_id)
    return



def main():
    naz=0
    markup=creaMark(1,'home',naz)
    while(True):
        @bot.message_handler(commands=['help','start'] )
        def send_welcome(msg):
            id=msg.chat.id
            bot.send_message(id,"ciao",reply_markup=markup)
        bot.polling(none_stop=True)
main()
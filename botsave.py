import config
import telebot
from telebot import types
import sqlite3
import sys

bot  = telebot.TeleBot(config.token)
shit = open('1500Book.pdf','rb')
cheap = open('cheap.pdf','rb')
chef = open('chefs.pdf','rb')
whole = open('wholefood.pdf','rb')

@bot.message_handler(commands=['start','this'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('books')
    markup.row('recepies')
    msg = bot.send_message(message.chat.id, "Hey dude, I can get some nice chef books or give my own recepies, what do u prefer? ", reply_markup=markup)
    bot.register_next_step_handler(msg, choice)

def choice(m):
    if m.text == 'books':
        bot.send_message(m.chat.id, 'look what can i give to u, maybe it will be useful',reply_markup=types.ReplyKeyboardRemove())
        bot.send_document(m.chat.id, shit )
        bot.send_document(m.chat.id, cheap )
        bot.send_document(m.chat.id, chef )
        bot.send_document(m.chat.id, whole )
        bot.send_message(message.chat.id, "press /this to try again")  
    elif m.text == 'recepies':
        bot.send_message(m.chat.id, 'wat do u want please tell me, u can choose main ingridient or type of your dish',reply_markup=types.ReplyKeyboardRemove())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['beef', 'poultry','seafood' ,'pork' ,'vegetable','eggs','breakfast','main dish','soup','salad', 'sweets']])
        bot.send_message(m.chat.id, 'what will u choose?',reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def handle_2(message):
    bot.send_message(message.chat.id, 'maybe it will be useful',reply_markup=types.ReplyKeyboardRemove())
    ingrid = str(message.text)
    ingrid = ingrid.lower()
    dbase = sqlite3.connect('database.db')
    with dbase:
        cur = dbase.cursor()
        cur.execute("SELECT recep FROM cookbook WHERE ingr = '%s'" %ingrid )
        rows = cur.fetchall()
        for row in rows:
            bot.send_message(message.chat.id, row)
    with dbase:
        cur = dbase.cursor()
        cur.execute("SELECT recep FROM cookbook WHERE type = '%s'" %ingrid )
        rows = cur.fetchall()
        for row in rows:
            bot.send_message(message.chat.id, row)
    dbase.close
    bot.send_message(message.chat.id, "press /this to try again")            
if __name__ == '__main__':
     bot.polling(none_stop=True)

import random

import telebot
import qrcode
from khayyam import JalaliDatetime
from gtts import gTTS
import pysynth_b

def user_age(year, month, day):
    days = JalaliDatetime.now() - JalaliDatetime(year, month, day)
    days = str(days).split(',')
    days = days[0].split(' ')
    age = int(days[0]) // 360
    return age

def text_to_voice(message_text):
    text = message_text
    language = 'en'
    myobj = gTTS(text= text, lang= language, slow= False)
    myobj.save('voice.ogg')

def show_max(message_text):
    array = message_text
    array = str(array).split(',')
    print(array)
    max = array[0]
    for i in range(1, len(array)):
        if int(array[i]) > int(max):
            max = array[i]
    return max

def send_max_index(message_text):
    array = message_text
    array = str(array).split(',')
    max = array[0]
    for i in range(1, len(array)):
        if int(array[i]) > int(max):
            max = array[i]
    return array.index(max)

def create_new_qrcode(message_text):
    str_text = message_text
    img = qrcode.make(str_text)
    img.save('qrcode.png')

mybot = telebot.TeleBot("TOKEN")

rand_num = random.randint(0, 15)

@mybot.message_handler(commands=['start'])
def send_welcome(message):
    mybot.reply_to(message,f"Hi {message.from_user.first_name}, Welcome\n/help- for commands")

@mybot.message_handler(commands=['game'])
def play_game(message):
    answer = mybot.reply_to(message, "Okay, Let's play a game, You should guess a number in range 0 ... 15, I will help you if your guess wasn't correct\nNow guess a number")
    mybot.register_next_step_handler(answer, get_num)

def get_num(message):
    global rand_num
    game_markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    btn1 = telebot.types.KeyboardButton('New Game')
    game_markup.add(btn1)
    
    game_markup_for_new_game = telebot.types.ReplyKeyboardMarkup(row_width=2)
    btn1 = telebot.types.KeyboardButton('New Game')
    btn2 = telebot.types.KeyboardButton('No')
    game_markup_for_new_game.add(btn1, btn2)

    if not message.text.startswith('/'):
        if message.text == 'New Game':
            rand_num = random.randint(0, 15)
            mybot.reply_to(message, "New game begin, Now guess a number", reply_markup= telebot.types.ReplyKeyboardRemove(selective=True))
            mybot.register_next_step_handler(message, get_num)
        
        elif message.text == 'No':
            mybot.send_message(message.chat.id, 'Ok, see you later', reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
        
        else:
            try:
                if int(message.text) == rand_num:
                    mybot.send_message(message.chat.id, 'Nice, You Win', reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
                    mybot.send_message(message.chat.id, 'New Game ?', reply_markup=game_markup_for_new_game)
                    mybot.register_next_step_handler(message, get_num)
                        

                elif int(message.text) < rand_num:
                    mybot.send_message(message.chat.id, 'Wrong, Go Upper', reply_markup=game_markup)
                    mybot.register_next_step_handler(message, get_num)
                
                elif int(message.text) > rand_num:
                    mybot.send_message(message.chat.id, 'Wrong, Go Lower', reply_markup=game_markup)
                    mybot.register_next_step_handler(message, get_num)
            except:
                mybot.send_message(message.chat.id, "Please just send 'Number' for me!")
    
    else:
        mybot.reply_to(message, 'I expect a number not a command.')
        mybot.send_message(message.chat.id, 'Now send me your command')

@mybot.message_handler(commands=['age'])
def send_user_age(message):
    answer = mybot.reply_to(message, 'Please enter your date of birth (YYYY/MM/DD)')
    mybot.register_next_step_handler(answer, get_date)

def get_date(message):
    if not message.text.startswith('/'):
        try:
            date = message.text
            date = str(date).split('/')
            date = user_age(date[0], date[1], date[2])
            mybot.send_message(message.chat.id, f"Your age is {date}")
        except:
            mybot.send_message(message.chat.id, 'Please enter your date of birth with the correct format (YYYY/MM/DD)')
    else:
        mybot.reply_to(message, 'I expect a number not a command')
        mybot.send_message(message.chat.id, 'Now send me your command')


@mybot.message_handler(commands=['voice'])
def get_voice(message):
    answer = mybot.reply_to(message, "Please type your sentence, Than i will convert it to voice (English only)")
    mybot.register_next_step_handler(answer, convet_voice)

def convet_voice(message):
    if not message.text.startswith('/'):
        text_to_voice(message.text)
        try:
            voice = open('voice.ogg', 'rb')
            mybot.send_audio(message.chat.id, voice)
        except:
            mybot.send_message(message.chat.id, 'Somthing went wrong, Please try again')
    else:
        mybot.reply_to(message, 'I expect a number not a command')
        mybot.send_message(message.chat.id, 'Now send me your command')
    

@mybot.message_handler(commands=['max'])
def get_array(message):
    answer = mybot.reply_to(message, 'Send me an Array and i will send the max number in that Array for you.\ncorrect format = num1,num2,num3,...')
    mybot.register_next_step_handler(answer, send_max)

def send_max(message):
    if not message.text.startswith('/'):
        max = show_max(message.text)
        mybot.send_message(message.chat.id, f"The Max number is : {max}")
    
    else:
        mybot.reply_to(message, 'I expect a number not a command')
        mybot.send_message(message.chat.id, 'Now send me your command')

@mybot.message_handler(commands=['argmax'])
def get_array(message):
    answer = mybot.reply_to(message, 'Send me an Array and i will send the Index of the max number in that Array for you.\ncorrect format = num1,num2,num3,...')
    mybot.register_next_step_handler(answer, send_index)

def send_index(message):
    if not message.text.startswith('/'):
        max_index = send_max_index(message.text)
        mybot.send_message(message.chat.id, f"The Index of the Max number is : {max_index}")
    
    else:
        mybot.reply_to(message, 'I expect a number not a command')
        mybot.send_message(message.chat.id, 'Now send me your command')

@mybot.message_handler(commands=['qrcode'])
def get_str(message):
    answer = mybot.reply_to(message, "Please enter a Sentence")
    mybot.register_next_step_handler(answer, create_qrcode)

def create_qrcode(message):
    if not message.text.startswith('/'):
        create_new_qrcode(message.text)
        try:
            img = open('qrcode.png', 'rb')
            mybot.send_photo(message.chat.id, img)
        except:
            mybot.send_message(message.chat.id, 'Somthing went wrong, Please try again')
    else:
        mybot.reply_to(message, 'I expect a number not a command')
        mybot.send_message(message.chat.id, 'Now send me your command')

@mybot.message_handler(commands=['music'])
def get_music(message):
    answer = mybot.reply_to(message, "enter your music note\nexample 1- ('c', 4), ('e', 4), ('g', 4), ('c5', -2), ('e6', 8), ('d#6', 2)\n\
example 2- ('c', 4), ('c*', 4), ('eb', 4), ('g#', 4), ('g*', 2), ('g5', 4), ('g5*', 4), ('r', 4), ('e5', 16), ('f5', 16), ('e5', 16), ('d5', 16), ('e5*', 4)")
    mybot.register_next_step_handler(answer, send_music)

def send_music(message):
    if not message.text.startswith('/'):
        try:
            song = eval(message.text)
            mybot.send_message(message.chat.id, 'Please wait ...')
            pysynth_b.make_wav(song, fn= 'song.wav')
            song_file = open('song.wav', 'rb')
            mybot.send_audio(message.chat.id, song_file)
        except:
            mybot.send_message(message.chat.id, 'Something went wrong, Please check the correct note format and try again')
    else:
        mybot.reply_to(message, 'I expect a number not a command')
        mybot.send_message(message.chat.id, 'Now send me your command')

@mybot.message_handler(commands=['help'])
def help_func(message):
    mybot.reply_to(message, "Here's the commands:\n/game- To play Number guessing game\n/age- To calculate your age\n/voice- To convert text to audio\
\n/max- To get the max number of an array\n/argmax- To get the index of the max number of an array\n/qrcode- To create a qrcode from a text\n/music- To create a song by sending song note")

@mybot.message_handler(func=lambda message: True)
def help(message):
    mybot.reply_to(message, "Please first select a command\n/help- for more information")

mybot.polling()
import telebot
from telebot import types # для указание типов 
import urllib.request, json 


token= #не скажу =)
bot=telebot.TeleBot(token)
flagShifr=False
sdvig=None
alfavit_RU = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
alfavit_dict = {alfavit_RU[i]:i for i in range(len(alfavit_RU))}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Шифр Цезаря")
    btn2 = types.KeyboardButton("Рандом пикча с собаками")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот. Выбери одну из моих функций.".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    global flagShifr
    global sdvig
    if (message.text == "Шифр Цезаря"):
        flagShifr=True
        bot.send_message(message.chat.id, text="Ввдите сдвиг ввиде числа от -15 до 15")
    elif message.text.lstrip("-").isdigit() and flagShifr and sdvig is None:
        ans=int(message.text)
        if -15 <= ans <= 15:
            sdvig=ans
            bot.send_message(message.chat.id, text="Ввдите сообщение которое нужно зашифровать")
        else:
            bot.send_message(message.chat.id, text="Ввдите сдвиг ввиде числа от -15 до 15")
    elif flagShifr and sdvig is not None:
        answer=""
        for i in message.text.upper():
            if i.isalpha():
                a = (alfavit_dict[i] + sdvig) % len(alfavit_RU)
                answer += alfavit_RU[a]
            else:
                answer += i
        flagShifr=False
        sdvig=None
        bot.send_message(message.chat.id, text = answer + "\nЧтобы вернуться в меню нажмите /start")
    elif (message.text == "Рандом пикча с собаками"):
        with urllib.request.urlopen("https://random.dog/woof.json") as url:
            data = json.load(url)
            bot.send_message(message.chat.id, text=data["url"])
    else:
        bot.send_message(message.chat.id, text="Я вас не понял \nЧтобы вернуться в меню нажмите /start")


bot.infinity_polling()
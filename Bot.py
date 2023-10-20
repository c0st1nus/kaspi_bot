import json
import random

import telebot
from telebot import types

bot = telebot.TeleBot('6198996168:AAH5oA_YT9n2UZMuKKfVcQmvflk_jm-zRhM')
chatID = None


def debug(message):
    textFile = open('Changes.txt', mode='a')
    textFile.write(message + '\n')
    textFile.close()


# noinspection PyTypeChecker
def send():
    global chatID
    textfile = open('Changes.txt', mode='r')
    text = textfile.read()
    textfile.close()
    if text:
        global chatID
        bot.send_message(chatID, text="Бот закончил анализ таблицы")
        with open('Changes.txt', 'rb') as document:
            bot.send_document(chatID, document)
    else:
        textfile = open('Changes.txt', mode='a')
        textfile.write('Нет изменений')
        textfile.close()
        bot.send_message(chatID, text="Бот закончил анализ таблицы")
        with open('Changes.txt', 'rb') as document:
            bot.send_document(chatID, document)
    print(chatID)


@bot.message_handler(commands=['start'])
def start(message):
    if message.text == '/start':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Зарегистрироваться', callback_data='Reg'),
                     types.InlineKeyboardButton('Авторизироваться', callback_data='Log'))
        bot.send_message(message.chat.id, "Здравствуйте! У вас есть аккаунт или вы здесь впервые?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'Reg':
        password = randompassword(8)
        bot.send_message(callback.message.chat.id, text=f'Регистрация успешно выполнена, ваш пароль: {password}')
        with open('UsersData/Users.json', 'r') as file:
            data = json.load(file)
        data['usernames'].append(f'{callback.message.from_user.id}')
        data['passwords'].append(f'{password}')
        with open('UsersData/Users.json', 'w') as file:
            json.dump(data, file)
    elif callback.data == 'Log':
        with open('UsersData/Users.json', 'r') as file:
            data = json.load(file)
        if f'{callback.message.from_user.id}' in data['usernames']:
            bot.send_message(callback.message.chat.id, text='Введите ваш пароль')
            bot.register_next_step_handler(callback.message, login, data['passwords'][data['usernames'].index(f'{callback.message.from_user.id}')])


def login(message, realPassword):
    if realPassword == message.text:
        bot.send_message(message.chat.id, 'Успешный вход')
    else:
        bot.send_message(message.chat.id, "Пароль не верный")
        bot.send_message(message.chat.id, 'Введите ваш пароль')
        bot.register_next_step_handler(message, login, realPassword)


def randompassword(count):
    randm = []
    for i in range(count):
        randm.append(str(random.randint(0, 10)))
    sep = ''
    return sep.join(randm)

if __name__ == "__main__":
    bot.polling(none_stop=True)

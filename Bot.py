import json
import random
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup
import os
from pathlib import Path
import openpyxl

bot = telebot.TeleBot('6198996168:AAH5oA_YT9n2UZMuKKfVcQmvflk_jm-zRhM')


@bot.message_handler(commands=['start'])
def start(message):
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if data != {"usernames": [], "passwords": [], "loginedUserID": []}:  # проверка на пустой json файл
        if f'{message.from_user.id}' in data['loginedUserID']:  # проверка на то, что пользователь ранее уже входил в аккаунт
            path = str(data["usernames"][data['loginedUserID'].index(str(message.from_user.id))]) #создаем config.json и 3 эксель файла если их нет
            if not Path(f'UsersData/{path}/config.json').is_file():
                with open(f'UsersData/{path}/config.json', 'w') as file:
                    data2 = {
                        'Login': None,
                        'Pass': None,
                        'Articles': [],
                        'excel_new_path': f'UsersData/{path}/new.xlsx',
                        'excel_old_path': f'UsersData/{path}/old.xlsx',
                        'excel_price_path': f'UsersData/{path}/price_new.xlsx'
                    }
                    json.dump(data2, file)
                if not Path(f'UsersData/{path}/new.xlsx').is_file():
                    workbook = openpyxl.Workbook()
                    sheet = workbook.active
                    sheet['A1'] = 'SKU'
                    sheet['B1'] = 'model'
                    sheet['D1'] = 'price'
                    sheet['K1'] = 'min price'
                    workbook.save(f'UsersData/{path}/new.xlsx')
                if not Path(f'UsersData/{path}/old.xlsx').is_file():
                    workbook = openpyxl.Workbook()
                    sheet = workbook.active
                    sheet['A1'] = 'id'
                    sheet['B1'] = 'title'
                    sheet['G1'] = 'link'
                    workbook.save(f'UsersData/{path}/old.xlsx')
                if not Path(f'UsersData/{path}/price_new.xlsx').is_file():
                    workbook = openpyxl.Workbook()
                    sheet = workbook.active
                    sheet['A1'] = 'SKU'
                    sheet['B1'] = 'model'
                    sheet['D1'] = 'price'
                    sheet['K1'] = 'min price'
                    workbook.save(f'UsersData/{path}/price_new.xlsx')  #создаем config.json и 3 эксель файла если их нет #создаем config.json и 3 эксель файла если их нет   #создаем config.json и 3 эксель файла если их нет
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton('Выйти'),)
            bot.send_message(message.chat.id, 'Здравствуйте!', reply_markup=keyboard)
            bot.register_next_step_handler(message, menu)
        else:
            keyboard: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton('Зарегистрироваться', callback_data='Reg'),
                         # иначе предложить ему регистрацию
                         types.InlineKeyboardButton('Авторизироваться', callback_data='Log'))
            bot.send_message(message.chat.id, "Здравствуйте! У вас есть аккаунт или вы здесь впервые?",
                             reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Зарегистрироваться', callback_data='Reg'),
                     types.InlineKeyboardButton('Авторизироваться', callback_data='Log'))
        bot.send_message(message.chat.id, "Здравствуйте! У вас есть аккаунт или вы здесь впервые?",
                         reply_markup=keyboard)


def menu(message):
    print('menu')
    keyboard = types.ReplyKeyboardMarkup()
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if message.text == '/start':
        bot.register_next_step_handler(message, start)
    elif message.text == 'Выйти':
        data['loginedUserID'][data['loginedUserID'].index(f'{message.from_user.id}')] = None
        bot.send_message(message.chat.id, 'Выход выполнен', reply_markup=keyboard)
    with open('UsersData/Users.json', 'w') as file:
        json.dump(data, file)


def login1(message):  # поиск логина в базе данных
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if message.text == '/start':
        bot.register_next_step_handler(message, start)
    elif message.text.lower() in data['usernames']:
        bot.send_message(message.chat.id, 'Введите ваш пароль')
        index = data['usernames'].index(message.text.lower())
        bot.register_next_step_handler(message, login2, index)
    else:
        bot.send_message(message.chat.id, 'Вы ввели не верный логин')
        bot.send_message(message.chat.id, 'Введите ваш логин')
        bot.register_next_step_handler(message, login1)


def login2(message, index):  # проверка пароля и сохранение айди пользователя в базе данных при положительном варианте
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if message.text == '/start':
        bot.register_next_step_handler(message, start)
    elif message.text == data['passwords'][index]:
        data['loginedUserID'][index] = str(message.from_user.id)
        with open('UsersData/Users.json', 'w') as file:
            json.dump(data, file)
        bot.send_message(message.chat.id, 'Вход выполнен')



def reg1(message):  # регистрация с генерацией пароля
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if message.text == '/start':
        bot.register_next_step_handler(message, start)
    elif message.text.lower() not in data['usernames']:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Сгенеренруй пароль из 8 чисел'))
        bot.send_message(message.chat.id, 'Введите пароль: ', reply_markup=keyboard)
        bot.register_next_step_handler(message, reg2, message.text)
    else:
        bot.send_message(message.chat.id, 'Пользователь с таким логином уже есть, попробуйте другой')
        bot.send_message(message.chat.id, 'Введите ваш логин')
        bot.register_next_step_handler(message, reg1)


def reg2(message, username):
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if message.text == '/start':
        bot.register_next_step_handler(message, start)
    elif message.text == 'Сгенеренруй пароль из 8 чисел':
        global password
        password = randompassword(8)
    else:
        password = message.text
    print(password)
    data['usernames'].append(username.lower())
    data['passwords'].append(password)
    data['loginedUserID'].append(f'{message.from_user.id}')
    bot.send_message(message.chat.id, f'Регистрация выполнена, ваш логин: {username}, ваш пароль: {password}')
    os.mkdir(f'UsersData/{username}')
    with open('UsersData/Users.json', 'w') as file:
        json.dump(data, file)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'Reg':
        bot.send_message(callback.message.chat.id, 'Введите ваш логин')
        bot.register_next_step_handler(callback.message, reg1)
    elif callback.data == 'Log':
        bot.send_message(callback.message.chat.id, 'Введите ваш логин')
        bot.register_next_step_handler(callback.message, login1)


def randompassword(count):
    randm = []
    for i in range(count):
        randm.append(str(random.randint(0, 10)))
    sep = ''
    return sep.join(randm)


if __name__ == "__main__":
    bot.polling(none_stop=True)

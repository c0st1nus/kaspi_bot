import json
import random
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup
import os
from pathlib import Path
import openpyxl
from kaspi.get import request
from user_agents.random_agnet import get_agent
from UsersData.Processing import loop
import UsersData.browser_bot
import threading

bot = telebot.TeleBot('6932808440:AAGsykujrc6eJ_V-_ULaNOL2afpXqriRbp8')


def my_background_function():
    while True:
        loop()


background_thread = threading.Thread(target=my_background_function)
background_thread.daemon = True
background_thread.start()


@bot.message_handler(commands=['start'])
def start(message):
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if data != {"usernames": [], "passwords": [], "loginedUserID": []}:  # проверка на пустой json файл
        if f'{message.from_user.id}' in data[
            'loginedUserID']:  # проверка на то, что пользователь ранее уже входил в аккаунт
            path = str(data["usernames"][data['loginedUserID'].index(
                str(message.from_user.id))])  # создаем config.json и 3 xlsx файла если их нет
            if not Path(f'UsersData/{path}/config.json').is_file():
                with open(f'UsersData/{path}/config.json', 'w') as file:
                    data2 = {
                        'Login': None,
                        'Pass': None,
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
                    workbook.save(
                        f'UsersData/{path}/price_new.xlsx')  # создаем config.json и 3 эксель файла если их нет #создаем config.json и 3 эксель файла если их нет   #создаем config.json и 3 эксель файла если их нет
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton('Выйти'), types.KeyboardButton('Добавить данные'),
                         types.KeyboardButton('Мои товары'), types.KeyboardButton('Запустить/Остановить работу бота'))
            bot.send_message(message.chat.id, 'Здравствуйте!', reply_markup=keyboard)
            index = data['loginedUserID'].index(str(message.from_user.id))
            bot.register_next_step_handler(message, menu, index)
        else:
            keyboard: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton('Зарегистрироваться', callback_data='Reg'),
                         types.InlineKeyboardButton('Авторизироваться', callback_data='Log'))
            bot.send_message(message.chat.id, "Здравствуйте! У вас есть аккаунт или вы здесь впервые?",
                             reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Зарегистрироваться', callback_data='Reg'),
                     types.InlineKeyboardButton('Авторизироваться', callback_data='Log'))
        bot.send_message(message.chat.id, "Здравствуйте! У вас есть аккаунт или вы здесь впервые?",
                         reply_markup=keyboard)


def productDelete(message, index):
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    with open(f'UsersData/{data["usernames"][index]}/config.json', 'r') as file:
        userdata = json.load(file)
    delete_row_by_value(userdata['excel_new_path'], message.text)
    bot.send_message(message.chat.id, 'Товар успешно удален')


def productAdd(message, index):
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    with open(f'UsersData/{data["usernames"][index]}/config.json', 'r') as file:
        userdata = json.load(file)
    listOfarticles = articles(userdata['excel_new_path'], 'A')
    if message.text in listOfarticles:
        bot.send_message(message.chat.id, 'Вы уже добавили этот товар')
    else:
        try:
            agent = get_agent()
            Reguest = request(message.text, agent)
            add_values_to_column(userdata['excel_new_path'],
                                 [message.text, Reguest["title"], Reguest["price"], Reguest["price"]],
                                 ['A', 'B', 'D', 'K'])
            add_values_to_column(userdata['excel_old_path'], [message.text, Reguest["title"]], ['A', 'B'])
            bot.send_message(message.chat.id, f'Товар({Reguest["title"]} - {Reguest["price"]} ₸) добавлен в писок')
        except:
            bot.send_message(message.chat.id, f'Вы ввели не правильное значение')


def product(message, index):
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    with open(f'UsersData/{data["usernames"][index]}/config.json', 'r') as file:
        userdata = json.load(file)
    if str(message.text) == 'Список товаров':
        if count_filled_cells(userdata['excel_new_path']) == 0:
            bot.send_message(message.chat.id, 'Вы не еще заполнили не одни товар')
        else:
            answer = ''
            result = count_filled_cells(userdata['excel_new_path'])
            for i in range(len(result)):
                if i != 0:
                    answer += str(result[i]) + '\n'
            bot.send_message(message.chat.id, text=answer)
    elif message.text == 'Удалить товар':
        bot.send_message(message.chat.id, 'Напшите артикул товара, который хотите удалить')
        bot.register_next_step_handler(message, productDelete, index)
    elif message.text == 'Добавить товар':
        bot.send_message(message.chat.id, 'Напшите артикул своего товара')
        bot.register_next_step_handler(message, productAdd, index)


def dataAdd(message, index):
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    with open(f'UsersData/{data["usernames"][index]}/config.json', 'r') as file:
        userdata = json.load(file)
    data2 = message.text.split(', ')
    if len(data2) != 2:
        bot.send_message(message.chat.id,
                         'Вы допустили ошибку при вводе данных, логин и пароль должны быть в одном сообщении через запятную(логин, пароль)')
    else:
        bot.send_message(message.chat.id, 'Бот пытается войти в ваш акаунт')
        if UsersData.browser_bot.try_to_sign_in_upload_kaspi(data2[0], data2[1]):
            bot.send_message(message.chat.id, 'Успешно, данные сохранены')
            userdata['Login'] = data2[0]
            userdata['Pass'] = data2[1]
            with open(f'UsersData/{data["usernames"][index]}/config.json', 'w') as file:
                json.dump(userdata, file)
        else:
            bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте еще раз')
            bot.send_message(message.chat.id,
                             'Введите логин и пароль от https://kaspi.kz/mc в ОДНОМ сообщении через запятую(логин, пароль)')
            bot.register_next_step_handler(message, dataAdd, index)


def menu(message, index):  # основное меню бота
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if message.text == '/start':
        bot.register_next_step_handler(message, start)
    elif message.text == 'Запустить/Остановить работу бота':
        with open(f'UsersData/{data["usernames"][index]}/config.json', 'r') as file:
            data2 = json.load(file)
        with open('UsersData/ReadyUsers.json', 'r') as file:
            data3 = json.load(file)
        if data['usernames'][index] not in data3['usernames']:
            if count_filled_cells(data2['excel_new_path']) != [] and data2['Login'] is not None:
                data3['usernames'].append(data['usernames'][index])
                with open('UsersData/ReadyUsers.json', 'w') as file:
                    json.dump(data3, file)
                bot.send_message(message.chat.id, 'Бот запущен')
            else:
                bot.send_message(message.chat.id, 'Не настроенны данные учетной записи либо не добавлены товары')
        else:
            data["usernames"].remove(data["usernames"][index])
            bot.send_message(message.chat.id, 'Бот отключен')

    elif message.text == 'Добавить данные':
        with open(f'UsersData/{data["usernames"][index]}/config.json', 'r') as file:
            userdata = json.load(file)
        if userdata['Login'] == None:
            bot.send_message(message.chat.id,
                             'Введите логин и пароль от https://kaspi.kz/mc в ОДНОМ сообщении через запятую(логин, пароль)')
            bot.register_next_step_handler(message, dataAdd, index)
        else:
            global s
            s = index
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton('Да', callback_data='changeKaspiData'),
                         types.InlineKeyboardButton('Нет, вернуться в меню', callback_data='ReturnToMainMenu'))
            bot.send_message(message.chat.id, 'У вас уже введены данные от Kaspi, вы хотите их изменить?1',
                             reply_markup=keyboard)
    elif message.text == 'Мои товары':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(types.KeyboardButton('Список товаров'))
        keyboard.row(types.KeyboardButton('Добавить товар'), types.KeyboardButton('Удалить товар'))
        bot.send_message(message.chat.id, 'Меню "Мои товары"', reply_markup=keyboard)
        bot.register_next_step_handler(message, product, index)
    elif message.text == 'Выйти':
        data['loginedUserID'][data['loginedUserID'].index(f'{message.from_user.id}')] = None
        bot.send_message(message.chat.id, 'Выход выполнен')
        with open('UsersData/Users.json', 'w') as file:
            json.dump(data, file)


def login1(message):  # поиск логина в Users.json
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


def login2(message, index):  # проверка пароля и сохранение айди пользователя в Users.json при положительном варианте
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if message.text == '/start':
        bot.register_next_step_handler(message, start)
    elif message.text == data['passwords'][index]:
        data['loginedUserID'][index] = str(message.from_user.id)
        with open('UsersData/Users.json', 'w') as file:
            json.dump(data, file)
        bot.send_message(message.chat.id, 'Вход выполнен')


def reg1(message):  # регистрация, логин
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


def reg2(message, username):  # регистрация, пароль вводится либо вручную либо бот генерирует случайный 8 значный пароль
    with open('UsersData/Users.json', 'r') as file:
        data = json.load(file)
    if message.text == '/start':
        bot.register_next_step_handler(message, start)
    elif message.text == 'Сгенеренруй пароль из 8 чисел':
        global password
        password = randompassword(8)
    else:
        password = message.text
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
    elif callback.data == 'changeKaspiData':
        global s
        with open('UsersData/Users.json', 'r') as file:
            data = json.load(file)
        with open(f'UsersData/{data["usernames"][s]}/config.json', 'r') as file:
            userdata = json.load(file)
        userdata['Login'] = None
        userdata['Pass'] = None
        with open(f'UsersData/{data["usernames"][s]}/config.json', 'w') as file:
            json.dump(userdata, file)
        print(s)
        bot.send_message(callback.message.chat.id,
                         'Введите логин и пароль от https://kaspi.kz/mc в ОДНОМ сообщении через запятую(логин, пароль)')
        bot.register_next_step_handler(callback.message, dataAdd, s)
    elif callback.data == 'ReturnToMainMenu':
        bot.send_message(callback.message.chat.id, 'Хорошо, пропишите /start')
        bot.register_next_step_handler(callback.message, start)


def randompassword(count):  # генерация пароля
    randm = []
    for i in range(count):
        randm.append(str(random.randint(0, 10)))
    sep = ''
    return sep.join(randm)


def articles(excel_path, sheetToAnalyze):
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook.active
    column_data_a = sheet[sheetToAnalyze]
    filled_cells = []
    for cell_a in column_data_a:
        if cell_a.value is not None:
            filled_cells.append(str(cell_a.value))
    if len(filled_cells) == 1:
        return []
    else:
        return (filled_cells)


def count_filled_cells(excel_path):
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook.active
    column_data_a = sheet['A']
    column_data_b = sheet['B']
    filled_cells = []

    for cell_a, cell_b in zip(column_data_a, column_data_b):
        if cell_a.value is not None and cell_b.value is not None:
            filled_cells.append(f'{cell_a.value}: {cell_b.value}')
    if len(filled_cells) == 1:
        return []
    else:
        return (filled_cells)


def add_values_to_column(excel_path, values_to_add, sheetsToAdd):
    workbook = openpyxl.load_workbook(excel_path)

    sheet = workbook.active
    column_data_a = sheet[sheetsToAdd[0]]
    place = str(len(column_data_a) + 1)
    for i in range(len(values_to_add)):
        sheet[sheetsToAdd[i] + place] = values_to_add[i]
    workbook.save(excel_path)
    workbook.close()


def delete_row_by_value(excel_path, value_to_delete):
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=1):
        for cell in row:
            if cell.value == value_to_delete:
                sheet.delete_rows(cell.row)
                break

    workbook.save(excel_path)
    workbook.close()


if __name__ == "__main__":
    bot.polling(none_stop=True)

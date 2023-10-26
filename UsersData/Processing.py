import json
import random
from time import sleep
from UsersData.document import excel_actions
from UsersData.browser_bot import sign_in_upload_kaspi
from kaspi.get import request
from user_agents.random_agnet import get_agent

def loop():
    with open('UsersData/ReadyUsers.json', 'r') as file:
        data = json.load(file)
    users = data['usernames']
    if len(users) == 0:
        print(f'Нет активных пользователей')
        print('===============================================')
        randm = random.randint(5, 15)
        print(f'Kaspi-Bot: Следующий старт через: {randm} сек.')
        sleep(randm)
    else:
        for i in users:
            print(f'Пользователь: {i}')
            print('===============================================')
            with open(f'UsersData/{i}/config.json', 'r') as file:
                userData = json.load(file)
            basic_bot_operation(i)
            excel_actions(action='cut', username=i)

            sign_in_upload_kaspi(username=i)
            sleep(2)
        randm = random.randint(10, 50)
        print(f'Kaspi-Bot: Следующий старт через: {randm} сек.')
        sleep(randm)
def basic_bot_operation(username):
    lists = excel_actions(action='select', username=username)
    data = []
    for lst in lists:
        filtered_lst = [item for item in lst if item is not None]
        data.append(filtered_lst)

    new_SKU = data[0]
    # new_price = data[1]
    # new_min_price = data[2]
    #
    # old_id = data[3]
    # old_link = data[4]

    cycle = 0
    colum_range = len(new_SKU) - 1

    print(f'Kaspi-Bot: В эксель файле {colum_range} артикулов.')

    for sku in new_SKU:
        cycle += 1
        print('===============================================')
        print(f'Цикл: {cycle} / {colum_range + 1}')

        str_sku = str(sku)

        handler(article=str_sku, username=username)

        #Генерируем рандомное время для ожидания между запросами на сайт kaspi.kz
        randm = random.randint(1, 3)
        print(f'Kaspi-Bot: Ожидаем: {randm} сек.')

        sleep(randm)


def handler(article, username):
    global_user_agent = get_agent()

    result = request(id_id=article, user_agent=global_user_agent)

    if result == 'error':
        print('Kaspi-Bot: Не удалось получить цену конкурентов.')
        sleep(1)

    else:
        excel_actions(action='update',
                      search_value=article,
                      web_price=result['price'],
                      username=username)

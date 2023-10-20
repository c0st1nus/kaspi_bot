import random
from time import sleep
from excel.document import excel_actions

from config import requests_end_range, requests_start_range, bot_op_start, bot_op_end

from kaspi.browser_bot import sign_in_upload_kaspi
from kaspi.get import request_price

from user_agents.random_agnet import get_agent

from Bot import debug
from datetime import datetime

# Бесконечний цикл.
# Сравнивает две таблицы, находит совпадения и передает их для дальнейшей обработки другой функции.

def loop():
    print("-------  Kaspi-Bot is running  -------")

    while True:
        # Обработка всей таблицы.
        basic_bot_operation()

        # Вырезка ненужных столбцов.
        excel_actions(action='cut')

        # Загрузка excel на kaspi
        sign_in_upload_kaspi()

        # Интервал между стартами.
        randm = random.randint(bot_op_start, bot_op_end)
        print(f'Kaspi-Bot: Следующий старт через: {randm} сек.')

        sleep(randm)


# В бесконечном цикле обработывается все задачи
def basic_bot_operation():
    lists = excel_actions(action='select')

    # Проходим по каждому списку и фильтруем значения None
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
        print(f'Цикл: {cycle} / {colum_range}')

        str_sku = str(sku)
        handler(article=str_sku)

        # Генерируем рандомное время для ожидания между запросами на сайт kaspi.kz
        randm = random.randint(requests_start_range, requests_end_range)
        print(f'Kaspi-Bot: Ожидаем: {randm} сек.')


        sleep(randm)


def handler(article):
    global_user_agent = get_agent()

    resault = request_price(id_id=article,
                            user_agent=global_user_agent)

    if resault == 'error':
        print('Kaspi-Bot: Не удалось получить цену конкурентов.')
        if(article != 'SKU'):
            now = datetime.now()
            formatted_date_time = now.strftime("%Y:%m:%d:%H:%M")
            debug(f'({formatted_date_time}) Article - {article}: Error: can\'t find price of competitor')
        sleep(1)

    else:
        excel_actions(action='update',
                      search_value=article,
                      web_price=resault)

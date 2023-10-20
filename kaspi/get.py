import requests
from datetime import datetime
from Bot import debug
def request_price(id_id, user_agent):

    print('Артикул:', id_id)
    parts = id_id.split("_")  # Разбиваем строку по символу "_"
    id = parts[0]  # Берем первую часть (до символа "_")


    url = f'https://kaspi.kz/yml/offer-view/offers/{id}'

    headers = {
        'Accept': 'application/json, text/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': f'{user_agent}',
        'Referer': f'{url}',
    }

    json_data = {
        'cityId': '750000000',
        'id': f'{id}',}

    response = requests.post(url=url, headers=headers, json=json_data)

    try:
        response_data = response.json()['offers'][0]['price']
        return int(response_data)

    except:
        print('Kaspi-Bot: Товар по артикулу не найден.')
        if(id_id != 'SKU'):
            now = datetime.now()
            formatted_date_time = now.strftime("%Y:%m:%d:%H:%M")
            debug(f'({formatted_date_time}) Article - {id_id}: Error: can\'t find an article')
        return 'error'


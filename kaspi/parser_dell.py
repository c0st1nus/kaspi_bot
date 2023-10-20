from contextlib import closing

from selenium import webdriver
from selenium.webdriver.common.by import By


def parsing(url, user_agent, headless):

    # Задаем настройки для браузера
    option = webdriver.FirefoxOptions()
    # Обход на проверку бота
    option.set_preference('dom.webdriver.enabled', False)
    # Отключаем левые уведомления в браузере
    option.set_preference('dom.webnotifications.enabled', False)
    # Настройка ЮзерАгента
    # option.set_preference('general.useragent.override', 'bu')
    option.add_argument(f'user-agent={user_agent}')
    # Прокси
    option.add_argument("--proxy-server=138.128.91.65:8000")

    # запуск в фоновом режиме
    if headless == 'yes':
        option.add_argument("--headless")


    with closing(webdriver.Firefox(options=option)) as browser:
        browser.get(url)

        # Ждёт 20 сек.
        browser.implicitly_wait(30)

        # Позиция кнопки X. (Окно: Выберите ваш город)
        xpatch = '/html/body/div[3]/div[1]/div/div[1]/div[2]/i'

        # Клик
        try:
            browser.find_element('xpath', xpatch).click()
        except:
            pass


        try:
            # Узнаем цену.
            button_price_str = browser.find_element(By.CLASS_NAME, 'item__price-once').text

            # Удаление пробелов и символа '₸' и преобразование в int
            button_price_int = int(button_price_str.replace(' ', '').replace('₸', ''))

            return button_price_int

        except:
            print('ОШИБКА ! Станицу не находит2.')
            return 'error'


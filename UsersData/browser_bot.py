import re
from contextlib import closing
from time import sleep
import os
from selenium import webdriver
from UsersData.handler import DatabaseHandler, db_connection
def try_to_sign_in_upload_kaspi(User_login, User_password) -> bool:

    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")

    with closing(webdriver.Firefox(options=option)) as browser:
        browser.get("https://kaspi.kz/mc/")
        browser.implicitly_wait(5)
        try:
            login_email_buttom_xpath = '//*[@id="email_tab"]'
            browser.find_element('xpath', login_email_buttom_xpath).click()

            email_input_xpath = '//*[@id="user_email_field"]'
            email_input = browser.find_element('xpath', email_input_xpath)
            email_input.send_keys(User_login)

            # Кликаем Продолжить
            continue_xpath = '/html/body/div/main/div/div/div/div[2]/section/section/form/button'
            browser.find_element('xpath', continue_xpath).click()

            # Вводим пароль
            password_xpath = '//*[@id="password_field"]'
            password_input = browser.find_element('xpath', password_xpath)
            password_input.send_keys(User_password)

            # Кликает на конпку Войти
            sign_in_xpath = '/html/body/div/main/div/div/div/div[2]/section/section/form/button'
            browser.find_element('xpath', sign_in_xpath).click()

            # Ожидаем загрузку страницы
            return True
        except Exception as e:
            print(e)

@db_connection
def sign_in_upload_kaspi(telegram_id, conn: DatabaseHandler):
    data = conn.query_data("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))[0]
    option = webdriver.FirefoxOptions()
    
    # option.add_argument("--headless")

    with closing(webdriver.Firefox(options=option)) as browser:
        browser.get("https://kaspi.kz/mc/")
        browser.implicitly_wait(5)
        try:

            login_email_buttom_xpath = '//*[@id="email_tab"]'
            browser.find_element('xpath', login_email_buttom_xpath).click()

            email_input_xpath = '//*[@id="user_email_field"]'
            email_input = browser.find_element('xpath', email_input_xpath)
            email_input.send_keys(data["login"])

            # Кликаем Продолжить
            continue_xpath = '/html/body/div/main/div/div/div/div[2]/section/section/form/button'
            browser.find_element('xpath', continue_xpath).click()

            # Вводим пароль
            password_xpath = '//*[@id="password_field"]'
            password_input = browser.find_element('xpath', password_xpath)
            password_input.send_keys(data["password"])

            # Кликает на конпку Войти
            sign_in_xpath = '/html/body/div/main/div/div/div/div[2]/section/section/form/button'
            browser.find_element('xpath', sign_in_xpath).click()

            # Ожидаем загрузку страницы
            
        except:
            print('ERROR | Kaspi-Bot: Станица для авторизации не найдена !')
        browser.get("https://kaspi.kz/mc/#/price-list")
        
        # Скролл
        browser.execute_script("window.scrollTo(0, 250)")

        excel_price_path = f'UsersData/{telegram_id}/pricelist.xlsx'
        absolute_path = os.path.abspath(excel_price_path)
        url = absolute_path.replace("/", "\\")
        # dell
        upload_xlxs = browser.find_element('xpath', "/html/body/div/section/div[2]/div/section/div/section/div[1]/div[2]/label/input")

        upload_xlxs.send_keys(url)

        upload_button_xpath = '/html/body/div/section/div[2]/div/section/div/section/div[1]/button'
        browser.find_element('xpath', upload_button_xpath).click()

        print('+++++++++++++++++++++++++++++++++++++++++++++++\n\n'
              'Kaspi-Bot: Загрузка прайс-листа успешно выполненa !\n\n'
              '+++++++++++++++++++++++++++++++++++++++++++++++')

@db_connection
def get_previous_upload_date(telegram_id, conn: DatabaseHandler):
    data = conn.query_data("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))[0]
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")

    with closing(webdriver.Firefox(options=option)) as browser:
        browser.get("https://kaspi.kz/mc/")
        browser.implicitly_wait(5)
        try:

            login_email_buttom_xpath = '//*[@id="email_tab"]'
            browser.find_element('xpath', login_email_buttom_xpath).click()

            email_input_xpath = '//*[@id="user_email_field"]'
            email_input = browser.find_element('xpath', email_input_xpath)
            email_input.send_keys(data["login"])

            # Кликаем Продолжить
            continue_xpath = '/html/body/div/main/div/div/div/div[2]/section/section/form/button'
            browser.find_element('xpath', continue_xpath).click()

            # Вводим пароль
            password_xpath = '//*[@id="password_field"]'
            password_input = browser.find_element('xpath', password_xpath)
            password_input.send_keys(data["password"])

            # Кликает на конпку Войти
            sign_in_xpath = '/html/body/div/main/div/div/div/div[2]/section/section/form/button'
            browser.find_element('xpath', sign_in_xpath).click()

            # Ожидаем загрузку страницы
            
        except:
            print('ERROR | Kaspi-Bot: Станица для авторизации не найдена !')
        browser.get("https://kaspi.kz/mc/#/history?page=1")
        first_element = browser.find_element('xpath', '/html/body/div/section/div[2]/div/section/div/div[1]/table/tbody/tr[2]/td[2]/div/a')
        first_element.click()

        date_paragraph = browser.find_element('xpath', '/html/body/div/section/div[2]/div/p')
        full_text = date_paragraph.text
        match = re.search(r'\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}', full_text)
        return match.group(0)

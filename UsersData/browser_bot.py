import json
from contextlib import closing
from time import sleep
import os
from selenium import webdriver


def try_to_sign_in_upload_kaspi(User_login, User_password):

    option = webdriver.FirefoxOptions()

    option.add_argument("--headless")

    with closing(webdriver.Firefox(options=option)) as browser:
        browser.get("https://kaspi.kz/mc/")
        sleep(5)
        try:

            # Нажимаем на Email
            login_email_buttom_xpath = '/html/body/div/div/div/div/div/form/div[1]/div/div/section/div/nav/ul/li[2]/a'
            # login_email_buttom_xpath = '/html/body/div/div/div/div/div/form/div[1]/div/div/section/div/nav/ul/li[2]/a/span'
            browser.find_element('xpath', login_email_buttom_xpath).click()

            sleep(2)

            # Вводим Email
            email_input_xpath = '//*[@id="user_email_field"]'
            email_input = browser.find_element('xpath', email_input_xpath)
            email_input.send_keys(User_login)

            sleep(2)

            # Кликаем Продолжить
            continue_xpath = '//*[@id="continue_button"]'
            browser.find_element('xpath', continue_xpath).click()

            # Вводим пароль
            password_xpath = '//*[@id="password_field"]'
            password_input = browser.find_element('xpath', password_xpath)
            password_input.send_keys(User_password)

            sleep(2)

            # Кликает на конпку Войти
            sign_in_xpath = '//*[@id="sign_in_button"]'
            browser.find_element('xpath', sign_in_xpath).click()

            # Ожидаем загрузку страницы
            sleep(5)
            return True
        except:
            return False


def sign_in_upload_kaspi(username):
    with open(f'UsersData/{username}/config.json') as file:
        data = json.load(file)
    option = webdriver.FirefoxOptions()

    option.add_argument("--headless")
    with closing(webdriver.Firefox(options=option)) as browser:
        browser.get("https://kaspi.kz/mc/")
        sleep(5)
        try:

            # Нажимаем на Email
            login_email_buttom_xpath = '/html/body/div/div/div/div/div/form/div[1]/div/div/section/div/nav/ul/li[2]/a'
            # login_email_buttom_xpath = '/html/body/div/div/div/div/div/form/div[1]/div/div/section/div/nav/ul/li[2]/a/span'
            browser.find_element('xpath', login_email_buttom_xpath).click()

            sleep(2)

            # Вводим Email
            email_input_xpath = '//*[@id="user_email_field"]'
            email_input = browser.find_element('xpath', email_input_xpath)
            email_input.send_keys(data['Login'])

            sleep(2)

            # Кликаем Продолжить
            continue_xpath = '//*[@id="continue_button"]'
            browser.find_element('xpath', continue_xpath).click()

            # Вводим пароль
            password_xpath = '//*[@id="password_field"]'
            password_input = browser.find_element('xpath', password_xpath)
            password_input.send_keys(data['Pass'])

            sleep(2)

            # Кликает на конпку Войти
            sign_in_xpath = '//*[@id="sign_in_button"]'
            browser.find_element('xpath', sign_in_xpath).click()

            # Ожидаем загрузку страницы
            sleep(5)
        except:
            print('ERROR | Kaspi-Bot: Станица для авторизации не найдена !')
        browser.get("https://kaspi.kz/mc/#/price-list")

        sleep(5)

        # Скролл
        browser.execute_script("window.scrollTo(0, 250)")

        excel_price_path = f'UsersData/{username}/price_new.xlsx'
        absolute_path = os.path.abspath(excel_price_path)
        url = absolute_path.replace("/", "\\")
        # dell
        upload_xlxs_xpath = '/html/body/div/div/section/div/div[2]/div/section[2]/div/section/div[1]/div[2]/label/input'
        upload_xlxs = browser.find_element('xpath', "//input[@type='file']")

        sleep(5)
        upload_xlxs.send_keys(url)

        sleep(2)

        upload_button_xpath = '//*[@id="app"]/div/section/div/div[2]/div/section[2]/div/section/div[1]/button/span'
        browser.find_element('xpath', upload_button_xpath).click()

        sleep(5)

        print('+++++++++++++++++++++++++++++++++++++++++++++++\n\n'
              'Kaspi-Bot: Загрузка прайс-листа успешно выполненa !\n\n'
              '+++++++++++++++++++++++++++++++++++++++++++++++')

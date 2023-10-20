# Путь к kaspi_bot
path_folder = 'D:\Projects\JetBrains'

# Путь к Excel файлам
excel_new_path = f'{path_folder}/kaspi_bot/excel/new.xlsx'
excel_old_path = f'{path_folder}/kaspi_bot/excel/old.xlsx'
excel_price_path = f'{path_folder}/kaspi_bot/excel/price_new.xlsx'

# Интервал в секундах между запросами. (Достаем цену конкурентов).
requests_start_range = 1
requests_end_range = 3

# На сколько Тенге будет снижать
x_tenge = 1

# Диапазон интервала в секундах: Между перерывами обработки таблицы, от начала до конца.
bot_op_start = 100
bot_op_end = 200

# Запуск браузера в фоновом режиме.
# Варианты: headless = 'no', headless = 'yes'
headless = 'yes'

# Данные для входа в kaspi
LOGIN = 'cybertechnologykz@gmail.com'
PASSWORD = 'Pasw0210r!d'

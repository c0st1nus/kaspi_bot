import telebot
import main.processing

bot = telebot.TeleBot('6198996168:AAH5oA_YT9n2UZMuKKfVcQmvflk_jm-zRhM')
chatID = '1239398217'


@bot.message_handler(commands=['start'])
def start(message):
    global ChatID
    bot.send_message(message.chat.id, f'Бот начал работу')
    main.processing.loop()

def debug(message):
    print(chatID)
    textFile = open('Changes.txt', mode='a')
    textFile.write(message + '\n')
    textFile.close()


def send():
    if chatID is not None:
        textfile = open('Changes.txt', mode='r')
        bot.send_message(chatID, text="Бот закончил анализ таблицы")
        bot.send_document(chatID, document=textfile)

if __name__ == "__main__":
    bot.polling(none_stop=True)

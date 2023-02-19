import telebot
from config import TOKEN, keys
from extensions import CurrencyConverter, ConvertException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def function_name(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'\t{message.chat.first_name}, приветствую!'
            'Этот бот поможет тебе узнать курс валюты и сконвертировать её. \n'
            'Чтобы начать, введи нужные валюты и укажи количество (Пример: рубль доллар 100).\n'
            'Если остались вопросы, используй команду /help')

@bot.message_handler(commands=['help'])
def start_help(message: telebot.types.Message):
    text = 'Для начала работы введите текст в следующем формате:\n' \
           'Имя валюты, цену которой хотите узнать;\n' \
           'Имя валюты, в которой надо узнать цену первой валюты;\n' \
           'Количество валюты.\n' \
           'Пример - рубль доллар 299\n' \
           'Посмотреть список доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты для конвертации:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertException('Неверное количество данных. Введите 3 параметра.')
        first_values, second_values, amount = values
        first_values = first_values.lower()
        second_values = second_values.lower()
        rate = CurrencyConverter.currency_convert(first_values, second_values, amount)
    except ConvertException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Ошибка!\n Не удалось обработать команду\n {e}')
    else:
        text = f'{amount} {first_values} = {round((rate * int(amount)), 6)} {second_values}'
        bot.send_message(message.chat.id, text)

bot.polling()

import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    username = message.from_user.username if message.from_user.username else "пользователь"
    text = f"👋 Приветствую, {username}! \n💲 Инструкция для работы с ботом /help"
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message):
    text = (
        "Чтобы начать работу, введите команду бота в следующем формате: \n"
        "<имя валюты> <в какую валюту перевести> <количество переводимой валюты> \n"
        "Например: \"USD EUR 10\". Чтобы увидеть список всех доступных валют: /values"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += f'\n{key}'
    bot.reply_to(message, text)

@bot.message_handler(commands=["convert"])
def command_handler(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Пожалуйста, введите ваш запрос в формате:\n<валюта> <валюта для конвертации> <количество>")

@bot.message_handler(func=lambda message: True)
def process_conversion(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        bot.reply_to(message, "Неверный формат запроса. Используйте: <валюта_1> <валюта_2> <количество>")
        return

    try:
        quote, base, amount = values

        if not amount.replace(',', '.').replace('.', '', 1).isdigit():
            raise APIException('Укажите корректное число.')

        amount = float(amount.replace(',', '.'))

        total_base = CryptoConverter.get_price(quote, base, amount)
        text = f'{amount} {quote} стоит {total_base} {base}'
        bot.send_message(message.chat.id, text)

    except APIException as e:
        bot.reply_to(message, f'Ошибка: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: {e}')

if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Начать взаимодействие с ботом"),
        telebot.types.BotCommand("/help", "Получить информацию о доступных командах"),
        telebot.types.BotCommand("/values", "Узнать доступные валюты"),
        telebot.types.BotCommand("/convert", "Узнать курс валюты")
    ])
    bot.polling()
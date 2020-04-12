import telebot
from WeatherManager import WeatherManager

import socks
import socket

from config import TelegramBotToken


def connect_proxy():
    '''
    Connecting through Tor, required
    Tor to be launched in this moment.
    '''
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
    socket.socket = socks.socksocket


connect_proxy()
oldcity_user = {}
weather_manager = WeatherManager()

bot = telebot.TeleBot(TelegramBotToken)

# Keyboards.
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Узнать текущую погоду')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Ввести новый город', 'Последний просмотренный город', 'Назад')


@bot.message_handler(commands=['start'])
def start_message(message):
    '''
    Starting menu for bot.
    :param message:
    :return:
    '''
    reply_start = "Привет, чтобы запустить бота напиши /start. \n" \
                  + "Чтобы узнать погоду жми на кнопки. \n" \
                  + "Для подробной информации напиши /help."

    bot.send_message(message.chat.id, reply_start, reply_markup=keyboard1)


@bot.message_handler(commands=['help'])
def help_message(message):
    '''
    Help menu for bot.
    :param message:
    :return:
    '''
    reply_help = "Привет, здесь ты можешь узнать прогноз погоды и" \
                 + " какую одежду тебе стоит надеть. \n" \
                 + "1. Чтобы начать работу жми на кнопку, какой" \
                 + " прогноз погоды ты хотел бы узнать. \n" \
                 + "2. После этого выбери тип каким образом " \
                 + "я смогу получить информацию о твоем местоположении. \n" \
                 + "3. В конце просто введи информацию о своем местоположении. \n"

    bot.send_message(message.chat.id, reply_help, reply_markup=keyboard1)


@bot.message_handler(func=lambda msg: msg.text == 'Узнать текущую погоду',
                     content_types=['text'])
def get_current_weather(message):
    '''
    Replying on request for current weather.
    :param message:
    :return:
    '''
    bot.send_message(message.chat.id, "Как я узнаю твой город?", reply_markup=keyboard2)
    bot.register_next_step_handler(message, process_city)


@bot.message_handler(func=lambda msg:
msg.text in {'Последний просмотренный город', 'Ввести новый город'},
                     content_types=['text'])
def get_current_weather(message):
    process_city(message)


def process_city(message):
    '''
    Processing message with type of getting city name.
    :param message:
    :return:
    '''
    if message.text == 'Ввести новый город':
        reply_info = "Хорошо, давай узнаем где тебе нужен прогноз погоды. \n" \
                     + "Напиши город. \n"
        bot.send_message(message.chat.id, reply_info)
        bot.register_next_step_handler(message, echo_weather, 'new_city')

    elif message.text == 'Последний просмотренный город':
        echo_weather(message, how='old_city')

    elif message.text == 'Назад':
        bot.send_message(message.chat.id, "Вернемся к погоде.", reply_markup=keyboard1)

    else:
        reply_notcorrect = "Я не понял что требуется, давай заново."
        bot.send_message(message.chat.id, reply_notcorrect, reply_markup=keyboard1)


def echo_weather(message, how):
    '''
    Sending weather result to user.
    :param message:
    :param how: what type of getting city
     if 'new_city' when will read cityname from message,
     if 'old_city' when using previous city of this user.
     Default city - 'Москва'.
    :return:
    '''
    if how == 'new_city':
        oldcity_user[message.chat.id] = message.text
        city = message.text
    elif how == 'old_city':
        if oldcity_user.get(message.chat.id) is None:
            city = 'Москва'  # Default city
        else:
            city = oldcity_user[message.chat.id]
    else:
        city = 'Москва'

    code, weather = weather_manager.get_weather(city)
    if code == 200:
        reply_weather = "Погода в " + city + " на данный момент \n" \
                        + "Температура  " + str(weather['temp']) + " по Цельсию \n" \
                        + "Ощущуается как " + str(weather['feels_like']) + "\n" \
                        + "Краткое описание: " + str(weather['descr']) + "\n" \
                        + "Давление " + str(weather['pressure']) + "мм ртутного столба \n" \
                        + "Влажность " + str(weather['humidity']) + "% \n" \
                        + "Скорость ветра " + str(weather['wind']) + "м/с \n"
    else:
        reply_weather = "К сожалению возникла ошибка " + str(code) + ": " + weather

    bot.send_message(message.chat.id, reply_weather)
    bot.send_message(message.chat.id, 'Можем повторить', reply_markup=keyboard1)


@bot.message_handler(func=lambda msg: msg.text == 'Назад',
                     content_types=['text'])
def get_previous(message):
    bot.send_message(message.chat.id, "Вернемся к погоде.", reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def echo_all(message):
    '''
    Reply on some text which is not command.
    :param message:
    :return:
    '''
    sticker_id = 'CAACAgIAAxkBAAMxXpGsmduSRc26Mt3KSYJn3p0xWI8AAgQAA4o3OAABcdDTag5yZuEYBA'
    reply_text = "Я тебя не понимаю, пиши /help, или жми на кнопки))"

    bot.send_sticker(message.chat.id, data=sticker_id)
    bot.send_message(message.chat.id, reply_text)


bot.polling(none_stop=True)
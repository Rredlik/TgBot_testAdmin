from telebot import types
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='HTML')


@bot.message_handler(commands=['start'])
async def start_message(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Админка", url='http://localhost')
    markup.add(button1)

    await bot.reply_to(message, '<b>Привет</b>, ты зарегистрирован!\n'
                                'Теперь ты будешь получать уведомления когда кто-то зайдет в админку.\n'
                                'Кстати ссылка на сайт в кнопке', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.send_message(message.chat.id, message.text)
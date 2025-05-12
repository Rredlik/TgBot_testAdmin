import asyncio
import logging
from datetime import datetime
from pprint import pprint

import telebot
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings

from core.apps.bot.middleware import CustomMiddleware
from core.apps.bot.models import TelegramUser
from services.database.bot_user_dao import get_all_telegram_users

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

bot.setup_middleware(middleware=CustomMiddleware())


# def generate_username(length=10):
#     return User.objects.make_random_password(length=length)


@bot.message_handler(commands=['start'])
async def start_message(message, data):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Админ-панель", url=settings.SITE_URL)
    markup.add(button1)
    text =  ('<b>Привет</b>, ты зарегистрирован!\n'
            'Теперь ты будешь получать уведомления когда кто-то зайдет в админку.\n'
            'Ссылка на сайт по кнопке')

    admin_username = data['admin_username']
    password = data['password']
    if data['is_new']:
        text += f'\n\nЛогин: <code>{admin_username}</code>\nПароль: <code>{password}</code>'

    await bot.reply_to(message, text, reply_markup=markup)


async def send_login_notification(tg_user):
    try:
        logger.debug('Getting all telegram users')
        # users = sync_to_async(TelegramUser.objects.all())
        users = await get_all_telegram_users()
        if not users:
            logger.warning("No users found for notification")
            return
        pprint(users)

        # Параллельная отправка через gather
        await asyncio.gather(*[
            send_single_notification(user.user_id, tg_user)
            for user in users
        ], return_exceptions=True)
    except Exception as e:
        logger.error(f"Notification error: {str(e)}")

async def send_single_notification(chat_id, tg_user):
    try:
        await bot.send_message(
            chat_id,
            f"⚠️ Вход в админку!\n"
            f"Пользователь: {tg_user.username} ({tg_user.user_id})\n"
            f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )
    except Exception as e:
        print(f"Ошибка отправки: {e}")


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.send_message(message.chat.id, message.text)
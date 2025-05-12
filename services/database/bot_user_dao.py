import logging
import random
import string

from asgiref.sync import sync_to_async
from django.contrib.auth import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from telebot import types

# from django.contrib.auth import models

from core.apps.bot.models import TelegramUser

logger = logging.getLogger(__name__)



def generate_password(length):
    characters = string.ascii_letters + string.digits # + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


@sync_to_async
def update_or_create_tg_user(data: types.Chat | types.User):
    try:
        data = getattr(data, 'chat')
    except AttributeError:
        data = data
    first_name = data.first_name
    if not data.first_name:
        first_name = ''

    username = data.username
    if not data.username:
        username = ''


    admin_username = f'{data.id}'
    # password = BaseUserManager().make_password(length=8)
    password = generate_password(10)
    password_hash = make_password(password)
    # user = models.User.objects.get_or_create(
    #     username=admin_username,
    #     password=password,
    #     is_staff=True  # Разрешаем доступ в админку
    # )
    # user, status = User.objects.get(username=admin_username)
    user, status = User.objects.get_or_create(username=admin_username,
                                              defaults= {'password': password_hash, 'is_staff': True})
                                          # password=password, is_staff=True)


    default_dict = {'user_id': data.id,
                    'full_name': first_name,
                    'username': username}
    telegram_user, create_status = TelegramUser.objects.update_or_create(django_user=user, create_defaults=default_dict)

    if create_status is False:
        logger.info(f'Успешно обновлен user в БД {data.id} - {first_name} ({username})')
    else:
        logger.info(f'Успешно создан user в БД {data.id} - {first_name} ({username})')
    return create_status, admin_username, password


@sync_to_async
def get_telegram_user(django_user):
    user = TelegramUser.objects.get(django_user=django_user)
    return user


@sync_to_async
def get_all_telegram_users():
    try:
        return list(TelegramUser.objects.all())
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return []
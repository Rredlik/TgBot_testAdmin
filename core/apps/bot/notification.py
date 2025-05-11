import logging

from asgiref.sync import async_to_sync
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from core.apps.bot.models import TelegramUser
from .main_bot import send_login_notification

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def handle_user_login(sender, request, user, **kwargs):
    try:
        # user = get_telegram_user(django_user=user)
        # async_to_sync(send_login_notification)(user)

        # Синхронное получение объекта TelegramUser
        tg_user = TelegramUser.objects.get(django_user=user)
        # Асинхронный вызов через event loop
        async_to_sync(send_login_notification)(tg_user.django_user)

    except TelegramUser.DoesNotExist:
        logger.error(f"TelegramUser not found for {user.username}")
    except Exception as e:
        logger.error(f"Login handler error: {str(e)}")
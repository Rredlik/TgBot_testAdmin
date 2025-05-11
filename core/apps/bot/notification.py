import asyncio

from asgiref.sync import sync_to_async
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from core.apps.bot.main_bot import send_login_notification
from core.apps.bot.models import TelegramUser

from asgiref.sync import async_to_sync



@receiver(user_logged_in)
def handle_user_login(sender, request, user, **kwargs):
    try:
        user = TelegramUser.objects.get(django_user=user)
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(send_login_notification(user))
        # loop.close()
        async_to_sync(send_login_notification)(user)
    except TelegramUser.DoesNotExist:
        pass
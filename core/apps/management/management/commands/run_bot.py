import asyncio

from django.core.management.base import BaseCommand

from core.apps.bot.main_bot import bot


class Command(BaseCommand):
    help = "Starts the Telegram-bot"

    def handle(self, *args, **options):
        asyncio.run(bot.polling())
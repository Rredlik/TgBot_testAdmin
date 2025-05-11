from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class TelegramUser(models.Model):
    """Пользователи телеграм бота"""
    user_id = models.PositiveBigIntegerField(_('ID Telegram User'), unique=True, primary_key=True, db_index=True)
    username = models.CharField(_('Username'), max_length=32)
    full_name = models.CharField(_('Full Name'), max_length=150)
    is_active = models.BooleanField(_('Is Active'), default=True)
    # django_user = models.OneToOneField()


    class Meta:
        verbose_name = _('Пользователь бота')
        verbose_name_plural = _('Пользователи бота')



from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

# Create your models here.


class TelegramUser(models.Model):
    """Пользователи телеграм бота"""
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True,)
    user_id = models.PositiveBigIntegerField(_('ID Telegram User'), unique=True, primary_key=True, db_index=True)
    full_name = models.CharField(_('Full Name'), max_length=150)
    username = models.CharField(_('Username'), max_length=32)
    is_active = models.BooleanField(_('Is Active'), default=True)

    # django_user = models.OneToOneField()

    def __str__(self):
        return f'{self.full_name} ({self.user_id})'

    class Meta:
        verbose_name = _('Пользователь бота')
        verbose_name_plural = _('Пользователи бота')

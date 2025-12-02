from django.contrib.auth.models import AbstractUser
from django.db import models

from telegram.constants import BOT_USER_DEFAULT_LANG
from birgo.constants import SUPPORTED_TEXT_LANGUAGES


class User(AbstractUser):
    """
    User model
    """
    is_welcomed = models.BooleanField(default=False)


class BotUser(models.Model):
    """
    Telegram bot user model
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    telegram_id = models.CharField(max_length=32)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    language_code = models.CharField(max_length=30, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    added_to_attachment_menu = models.BooleanField(default=False)
    allows_write_to_pm = models.BooleanField(default=False)
    photo_url = models.URLField(blank=True, null=True)
    birthday = models.JSONField(default=dict, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    status = models.BooleanField(default=True)
    has_left = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_display_name(self) -> str:
        """ get Bot user's full name (shorter) """
        display_name = self.first_name
        if self.last_name:
            display_name += f" {self.last_name}"
        return display_name[:40]

    def get_lang(self) -> str:
        """ get Bot user's language code: ru|uz|en|... """
        lang = BOT_USER_DEFAULT_LANG
        if self.language_code in SUPPORTED_TEXT_LANGUAGES:
            lang = self.language_code
        return lang

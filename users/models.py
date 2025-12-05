from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from birgo.classes.models import BaseModelInterface
from birgo.constants import SUPPORTED_TEXT_LANGUAGES
from telegram.constants import BOT_USER_DEFAULT_LANG


class User(AbstractUser):
    """
    User model
    """
    USER_GENDER_CHOICES = (
        ("m", _("Male")),
        ("f", _("Female"))
    )
    is_welcomed = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=USER_GENDER_CHOICES,
                              blank=True, null=True)

    def get_shortened_name(self) -> str:
        name = self.first_name
        if len(self.first_name) > 12:
            name = name[:12]
        return name

    def get_driver(self):
        return self.driver_set.filter(approved_at__isnull=False).last()


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


class UserLocation(models.Model, BaseModelInterface):
    """ User locations (addresses) model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    region = models.ForeignKey("system.Region", on_delete=models.SET_NULL, null=True, blank=True)
    coordinates = models.JSONField(default=dict, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

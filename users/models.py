from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User model
    """


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

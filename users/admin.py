import telebot
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User, BotUser


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """ User model admin class """
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    """ BotUser model admin class """
    list_display = ('id', 'get_display_name', 'username', 'allows_write_to_pm',
                    'status', 'has_left', 'date_created')
    list_filter = ('status', 'has_left', 'allows_write_to_pm', 'date_created')
    search_fields = ('id', 'first_name', 'last_name', 'username', 'telegram_id')
    actions = ('update_bot_user_data',)

    @admin.action(description='Update Telegram bot user data')
    def update_bot_user_data(self, request, queryset):
        """ method for updating BotUser's data using Telegram API """
        bot = telebot.TeleBot(settings.BOT_TOKEN)
        for bu in queryset:
            bu: BotUser
            try:
                data = bot.get_chat(bu.telegram_id)
                bu.first_name = data.first_name
                bu.last_name = data.last_name
                bu.username = data.username
                bu.has_left = False
                bu.personal_chat = {
                    "id": data.personal_chat.id,
                    "title": data.personal_chat.title,
                    "description": data.personal_chat.description,
                    "username": data.personal_chat.username,
                    "is_forum": data.personal_chat.is_forum,
                    "type": data.personal_chat.type,
                } if data.personal_chat else None
                bu.birthday = data.birthdate.__dict__ if data.birthdate else None
                bu.bio = data.bio
                bu.save()
            except telebot.apihelper.ApiException as e:
                messages.error(request, str(e))

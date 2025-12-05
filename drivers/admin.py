from django.conf import settings
from django.contrib import admin
from telebot import TeleBot, types

from drivers.models import Driver, Car
from telegram.texts import open_button_text, noty_to_new_driver


class DriverCarInline(admin.TabularInline):
    """ Driver's cars inline for DriverAdmin """
    model = Car
    extra = 0


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """ Driver model admin class """
    list_display = ("id", "user", "status", "created_at", "approved_at")
    list_filter = ("created_at", "approved_at", "status")
    search_fields = ("id",)
    inlines = (DriverCarInline,)
    actions = ["send_registering_success_notifications"]

    @admin.action(description='Отправить уведомление о том что был подключен как водитель')
    def send_registering_success_notifications(self, request, queryset):
        for dr in queryset:
            dr: Driver
            if dr.approved_at:
                bot_user_lang = dr.user.botuser.get_lang()

                bot = TeleBot(token=settings.TELEGRAM_BOT_TOKEN)
                msg_reply_markup = types.InlineKeyboardMarkup(row_width=1)
                url = f"https://t.me/bir_go_bot/app"
                msg_reply_markup.add(
                    types.InlineKeyboardButton(
                        open_button_text.get(bot_user_lang),
                        url=url
                    )
                )

                noty_text = noty_to_new_driver.get(bot_user_lang)
                bot.send_message(
                    dr.user.botuser.telegram_id,
                    noty_text,
                    parse_mode="HTML",
                    reply_markup=msg_reply_markup,
                )

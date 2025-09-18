from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _, get_language

from init_data_py import InitData
import init_data_py.errors

from telegram.decorators import tg_pages
from users.models import BotUser

def init(request):
    page_title = _("Init page")
    start_param = request.GET.get('tgWebAppStartParam', None)
    return render(request, "tg-mini-app/init.html", locals())

@tg_pages("Home")
def home(request, bot_user: BotUser, *args, **kwargs):
    print(bot_user)
    return render(request, "tg-mini-app/home.html", locals() | kwargs)

@tg_pages("Error on validating auth data")
def aut_error(request, bot_user, *args, **kwargs):
    error_title = kwargs.pop('page_title', None)
    return render(request, "tg-mini-app/errors/error_page.html", locals() | kwargs)

def validate_user(request):
    if request.GET.get("signature"):
        data = request.GET.copy()
        safe_data = data.urlencode()
        try:
            init_data = InitData.parse(safe_data)
        except init_data_py.errors.errors.UnexpectedFormatError as e:
            return redirect("tg_auth_error")
        if init_data.validate(bot_token=settings.BOT_TOKEN):
            bot_user, is_new = BotUser.objects.get_or_create(
                telegram_id=init_data.user.id,
            )
            bot_user.first_name = init_data.user.first_name
            bot_user.last_name = init_data.user.last_name
            bot_user.username = init_data.user.username
            if init_data.user.is_premium:
                bot_user.is_premium = init_data.user.is_premium
            bot_user.language_code = init_data.user.language_code
            if init_data.user.added_to_attachment_menu:
                bot_user.added_to_attachment_menu = init_data.user.added_to_attachment_menu
            if init_data.user.allows_write_to_pm:
                bot_user.allows_write_to_pm = init_data.user.allows_write_to_pm
            bot_user.photo_url = init_data.user.photo_url
            bot_user.save()
            data = init_data.to_dict()
            data["bot_user_id"] = bot_user.id
            request.session["init_data"] = data
            return redirect("tg_home") # author's cabinet
    return redirect("tg_auth_error")
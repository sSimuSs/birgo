from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from init_data_py import InitData
import init_data_py.errors

from lots.models import UserLot
from telegram.decorators import tg_pages
from users.models import BotUser

def init(request):
    """
    Initial page view for Telegram Mini App.
    It will get Mini App's init data in js and will redirect to tg_validate_user page
    """
    page_title = _("Init page")
    start_param = request.GET.get('tgWebAppStartParam', None)
    return render(request, "tg-mini-app/init.html", locals())

@tg_pages("Home")
def home(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app home page view """
    lots = UserLot.objects.filter(status=5)
    return render(request, "tg-mini-app/home.html", locals() | kwargs)

def aut_error(request, *args, **kwargs):
    """ Error page view for 'Authentication Error' """
    page_title = _("Error on validating auth data")
    error_title = page_title
    return render(request, "tg-mini-app/errors/error_page.html", locals() | kwargs)

def validate_user(request):
    """ Middleware view for handling Telegram's initData from Mini App """
    if request.GET.get("signature"):
        data = request.GET.copy()
        safe_data = data.urlencode()

        try:
            init_data = InitData.parse(safe_data)
        except init_data_py.errors.errors.UnexpectedFormatError:
            return redirect("tg_auth_error")

        if init_data.validate(bot_token=settings.TELEGRAM_BOT_TOKEN):
            bot_user, __ = BotUser.objects.get_or_create(
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

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from init_data_py import InitData
import init_data_py.errors

from lots.models import UserLot, UserLotCategory
from telegram.decorators import tg_pages
from users.models import BotUser, User


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
    lots = UserLot.objects.filter(status=5).order_by("-id")
    kwargs['back_button_url'] = None
    if not bot_user.user.is_welcomed:
        return redirect("tg_welcome")
    return render(request, "tg-mini-app/home.html", locals() | kwargs)

@tg_pages("User")
def user_detail(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app user detail page view """
    user = get_object_or_404(User, id=kwargs['pk'])
    kwargs["page_title"] += f": {user.botuser.get_display_name()}"

    section = request.GET.get("section", "lots")
    match section:
        case "lots":
            lots = user.userlot_set.order_by("-id")
        case "offers":
            offers = user.offer_set.order_by("-id")
    print(bot_user)
    return render(request, f"tg-mini-app/user/{section}.html", locals() | kwargs)

@tg_pages("Wish")
def lot_detail(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app user detail page view """
    lot: UserLot = get_object_or_404(UserLot, pk=kwargs["pk"])
    kwargs["page_title"] += f": {lot.title}"
    lot_cats = lot.get_cats(bot_user.get_lang())

    lot_offers = lot.offer_set.order_by("-price")
    return render(request, "tg-mini-app/lots/detail.html", locals() | kwargs)

@tg_pages("Category")
def cat_page(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app user detail page view """
    category: UserLotCategory = get_object_or_404(UserLotCategory, slug=kwargs["slug"])
    cat_name = category.get_name(bot_user.get_lang())
    kwargs["page_title"] += f": {cat_name}"
    return render(request, "tg-mini-app/cats/detail.html", locals() | kwargs)

@tg_pages("Welcome to Wishr!")
def welcome(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app Welcome page view """
    kwargs['back_button_url'] = None
    bot_user.user.is_welcomed = True
    bot_user.user.save()
    return render(request, "tg-mini-app/welcome.html", locals() | kwargs)

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
            bot_user, is_new_user = BotUser.objects.get_or_create(
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

            if is_new_user:
                username = f"user{init_data.user.id}"
                if init_data.user.username:
                    username = init_data.user.username

                user = User.objects.create(
                    first_name=init_data.user.first_name,
                    last_name=init_data.user.last_name,
                    username=username,
                )
                bot_user.user = user
                bot_user.save()

            data = init_data.to_dict()
            data["bot_user_id"] = bot_user.id
            request.session["init_data"] = data
            return redirect("tg_home") # author's cabinet
    return redirect("tg_auth_error")

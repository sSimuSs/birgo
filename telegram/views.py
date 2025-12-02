from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from init_data_py import InitData
import init_data_py.errors

from telegram.decorators import tg_pages
from users.models import BotUser, User
from birgo.functions import slugify, get_random_integer


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

@tg_pages("Create a new lot")
def lot_create(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app creation a new lot page view """
    if request.method == "POST":
        data = request.POST.copy()
        form = UserLotForm(data=data)
        if form.is_valid():
            form.instance.user_id = bot_user.user_id
            form.instance.slug = f"{slugify(form.instance.title)}{get_random_integer(4)}"
            lot = form.save()
            if request.FILES:
                gallery_form = LotGalleryForm(request.POST, request.FILES)
                if gallery_form.is_valid():
                    gallery_form.instance.lot_id = lot.id
                    gallery_form.instance.main = True
                    image = gallery_form.save()
            return redirect("tg_home")
        else:
            errors = form.errors.as_data()

    return render(request, "tg-mini-app/lots/create.html", locals() | kwargs)

@tg_pages("Editing a lot")
def lot_edit(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app editing a lot page view """
    lot: UserLot = get_object_or_404(UserLot, pk=kwargs["pk"])
    kwargs["page_title"] += f": {lot.title}"

    if request.method == "POST":
        data = request.POST.copy()
        clear_image = data.pop("clear_image")[0] == "1"
        form = UserLotForm(instance=lot, data=data)
        if form.is_valid():
            lot = form.save()
            if request.FILES:
                gallery_form = LotGalleryForm(request.POST, request.FILES)
                if gallery_form.is_valid():
                    lot.userlotgallery_set.filter(main=True).delete()

                    gallery_form.instance.lot_id = lot.id
                    gallery_form.instance.main = True
                    image = gallery_form.save()
            elif clear_image:
                lot.userlotgallery_set.filter(main=True).delete()
            return redirect("tg_home")
        else:
            errors = form.errors.as_data()

    return render(request, "tg-mini-app/lots/edit.html", locals() | kwargs)

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

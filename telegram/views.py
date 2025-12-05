import phonenumbers
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from init_data_py import InitData
import init_data_py.errors

from birgo.constants import ENV_PRODUCTION
from drivers.models import Driver
from system.models import Region
from telegram.decorators import tg_pages
from trips.models import TripRequest
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

    kwargs['back_button_url'] = None
    if not bot_user.user.is_welcomed:
        return redirect("tg_welcome")

    draft_trip_request, __ = bot_user.user.triprequest_set.get_or_create(
        sent_at__isnull=True, canceled_at__isnull=True
    )

    sent_trip_requests = bot_user.user.triprequest_set.filter(
        canceled_at__isnull=True, sent_at__isnull=False
    )
    if request.method == "POST":
        cost = request.POST.get("cost")
        comments = request.POST.get("comments")
        draft_trip_request.cost = cost
        draft_trip_request.comments = comments
        draft_trip_request.save()
        if not draft_trip_request.submit_trip_request():
            pass
        return redirect("tg_trip_request", pk=draft_trip_request.pk)
    return render(request, "tg-mini-app/home.html", locals() | kwargs)

@tg_pages("User")
def user_detail(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app user detail page view """
    user = get_object_or_404(User, id=kwargs['pk'])
    kwargs["page_title"] += f": {user.botuser.get_display_name()}"
    print(bot_user)

    section = request.GET.get("section", "details")
    # match section:
    #     case "lots":
    #         lots = user.userlot_set.order_by("-id")
    #     case "offers":
    #         offers = user.offer_set.order_by("-id")
    return render(request, f"tg-mini-app/user/{section}.html", locals() | kwargs)


@tg_pages("Welcome to BirGo!")
def welcome(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app Welcome page view """
    kwargs['back_button_url'] = None
    bot_user.user.is_welcomed = True
    bot_user.user.save()
    return render(request, "tg-mini-app/welcome.html", locals() | kwargs)

@tg_pages("Driver page")
def driver_page(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app Driver page view """
    kwargs['back_button_url'] = None
    driver = bot_user.user.get_driver()
    if request.GET.get("toggle_status"):
        driver.status = 0 if driver.status else 1
        driver.save()
        return redirect("tg_driver_page")

    if driver.status == 1:
        trip_requests = TripRequest.objects.filter(
            ~Q(user=bot_user.user), canceled_at__isnull=True, sent_at__isnull=False
        )
    return render(request, "tg-mini-app/drivers/main.html", locals() | kwargs)

@tg_pages("Searching for a car")
def trip_request(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app Welcome page view """
    t_request = TripRequest.objects.filter(sent_at__isnull=False, id=kwargs['pk']).last()
    if not t_request:
        return redirect("tg_home")

    is_owner = True
    if t_request.user != bot_user.user:
        is_owner = False
        driver = bot_user.user.get_driver()
        if driver and driver.status == 1:
            kwargs['back_button_url'] = reverse("tg_driver_page")
            driver.triprequestview_set.get_or_create(
                trip_request=t_request,
            )
        else:
            return redirect("tg_home")

    if is_owner and request.GET.get("cancel_trip_request"):
        t_request.cancel_trip_request()
        return redirect("tg_home")
    return render(request, "tg-mini-app/trips/trip_request.html", locals() | kwargs)

@tg_pages("How many people?")
def select_people_count(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app selecting people count page view """
    if request.GET.get("select") and request.GET["select"].isdigit():
        draft_trip_request, __ = bot_user.user.triprequest_set.get_or_create(
            sent_at__isnull=True, canceled_at__isnull=True
        )
        draft_trip_request.people_count = int(request.GET.get("select"))
        draft_trip_request.save()
        return redirect("tg_home")
    return render(request, "tg-mini-app/trips/select_people_count.html", locals() | kwargs)

@tg_pages("Selecting a region for the trip")
def select_region(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app Selecting region for a draft trip page view """
    location_type = request.GET.get("location_type", "start") # start|finish
    draft_trip_request, __ = bot_user.user.triprequest_set.get_or_create(
        sent_at__isnull=True, canceled_at__isnull=True
    )

    regions = Region.objects.filter(status=True)
    if location_type == "start" and draft_trip_request.region_b:
        if draft_trip_request.region_b.parent:
            regions = regions.filter(
                ~Q(id=draft_trip_request.region_b.parent_id),
                ~Q(parent_id=draft_trip_request.region_b.parent_id)
            )
        else:
            regions = regions.filter(
                ~Q(id=draft_trip_request.region_b_id)
            )
    elif location_type == "finish" and draft_trip_request.region_a:
        if draft_trip_request.region_a.parent:
            regions = regions.filter(
                ~Q(id=draft_trip_request.region_a.parent_id),
                ~Q(parent_id=draft_trip_request.region_a.parent_id)
            )
        else:
            regions = regions.filter(
                ~Q(id=draft_trip_request.region_a_id)
            )


    if request.GET.get("select"):
        region_id = request.GET["select"]
        region = Region.objects.filter(id=region_id).last()
        if region and region.sub_regions_count() == 0:
            if location_type == "finish":
                draft_trip_request.region_b = region
            else:
                draft_trip_request.region_a = region
            draft_trip_request.save()
            return redirect("tg_home")

    if request.GET.get("parent"):
        kwargs['back_button_url'] = reverse("tg_select_region") + f"?location_type={location_type}"
        regions = regions.filter(parent_id=request.GET["parent"])
    else:
        regions = regions.filter(parent__isnull=True)
    return render(request, "tg-mini-app/trips/select_region.html", locals() | kwargs)

@tg_pages("Registering a new driver")
def driver_register(request, bot_user: BotUser, *args, **kwargs):
    """ Telegram Mini app New driver page view """

    driver = bot_user.user.driver_set.last()

    if driver:
        first_name = driver.user.first_name
        last_name = driver.user.last_name
        phone = driver.user.phone

    if request.method == "POST":
        errors = {}
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        if phone:
            phone = phone.replace("-", "").replace(" ", "")
        else:
            errors["phone"] = _("Phone number is required")

        try:
            number = phonenumbers.parse(phone)
            if not phonenumbers.is_possible_number(number) or not phonenumbers.is_valid_number(number):
                errors["phone"] = _("Incorrect phone number")
        except phonenumbers.NumberParseException as e:
            errors["phone"] = _("Incorrect phone number")

        if not errors and phone and first_name and last_name:
            username = f"user{bot_user.telegram_id}"
            if bot_user.username:
                username = bot_user.username

            if bot_user.user.first_name != first_name:
                bot_user.user.first_name = first_name
            if bot_user.user.last_name != last_name:
                bot_user.user.last_name = last_name
            if bot_user.user.phone != phone:
                bot_user.user.phone = phone.replace("+", "")
            if bot_user.user.username != username:
                bot_user.user.username = username
            bot_user.user.save()

            if not driver:
                driver = Driver.objects.create(
                    user=bot_user.user,
                )
                # if settings.ENV == ENV_PRODUCTION:
                driver.send_to_staff_channel()
            return redirect("tg_driver_register")
    return render(request, "tg-mini-app/drivers/register.html", locals() | kwargs)

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
            if init_data.start_param:
                if init_data.start_param == "new_driver":
                    return redirect("tg_driver_register")
            if bot_user.user.get_driver():
                return redirect("tg_driver_page") # driver's cabinet
            return redirect("tg_home") # passenger's cabinet
    return redirect("tg_auth_error")

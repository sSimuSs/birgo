from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy

from users.models import BotUser


def tg_pages(page_title_en: str):
    """ decorator from telegram mini app page views """
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            kwargs['page_title'] = gettext_lazy(page_title_en)

            user_id = 1
            if settings.ENV != "develop":
                user_data = request.session.get("init_data")
                if user_data is None:
                    return redirect("tg_auth_error")
                user_id = user_data["bot_user_id"]
            bot_user: BotUser = get_object_or_404(BotUser, id=user_id)
            return view_func(request, bot_user, *args, **kwargs)
        return wrap
    return decorator

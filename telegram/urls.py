from django.urls import path
from django.conf.urls.i18n import i18n_patterns

from telegram.views import (
    home, user_detail, lot_detail,
    aut_error, init, validate_user, cat_page, welcome, lot_create
)

urlpatterns = i18n_patterns(
    path('tg/init/', init, name='tg_init'),
    path('tg/', home, name='tg_home'),
    path('tg/welcome', welcome, name='tg_welcome'),
    path('tg/user/<int:pk>', user_detail, name='tg_user_detail'),
    path('tg/cats/<str:slug>', cat_page, name='tg_cat_page'),
    path('tg/lots/<int:pk>', lot_detail, name='tg_lot_detail'),
    path('tg/lots/create', lot_create, name='tg_lot_create'),
    path('tg/auth_error/', aut_error, name='tg_auth_error'),
) + [path('tg/validate_user/', validate_user, name="validate_user")]

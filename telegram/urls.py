from django.urls import path
from django.conf.urls.i18n import i18n_patterns

from telegram.views import (
    home, user_detail, lot_detail,
    aut_error, init, validate_user
)

urlpatterns = i18n_patterns(
    path('tg/init/', init, name='tg_init'),
    path('tg/', home, name='tg_home'),
    path('tg/user/<int:pk>', user_detail, name='tg_user_detail'),
    path('tg/lots/<int:pk>', lot_detail, name='tg_lot_detail'),
    path('tg/auth_error/', aut_error, name='tg_auth_error'),
) + [path('tg/validate_user/', validate_user, name="validate_user")]

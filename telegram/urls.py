from django.urls import path
from django.conf.urls.i18n import i18n_patterns

from telegram.views import (
    home, user_detail,
    aut_error, init, validate_user, welcome, select_region,
    select_people_count, trip_request, driver_register,
    driver_page
)

urlpatterns = i18n_patterns(
    path('tg/init/', init, name='tg_init'),
    path('tg/', home, name='tg_home'),
    path('tg/welcome', welcome, name='tg_welcome'),
    path('tg/driver_page', driver_page, name='tg_driver_page'),
    path('tg/trip_request/<int:pk>', trip_request, name='tg_trip_request'),
    path('tg/select_region', select_region, name='tg_select_region'),
    path('tg/select_people_count', select_people_count, name='tg_select_people_count'),
    path('tg/driver_register', driver_register, name='tg_driver_register'),
    path('tg/user/<int:pk>', user_detail, name='tg_user_detail'),
    path('tg/auth_error/', aut_error, name='tg_auth_error'),
) + [path('tg/validate_user/', validate_user, name="validate_user")]

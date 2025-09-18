from django.urls import path

from telegram.views import (
    home, aut_error, init
)

urlpatterns = [
    path('tg/init/', init, name='tg_init'),
    path('tg/', home, name='tg_home'),
    path('tg/auth_error/', aut_error, name='tg_auth_error'),
]

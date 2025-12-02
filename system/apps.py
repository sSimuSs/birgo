from django.apps import AppConfig


class SystemConfig(AppConfig):
    """ system app config """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'system'

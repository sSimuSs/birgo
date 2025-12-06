from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from telebot import TeleBot

from birgo.classes.models import BaseModelInterface
from drivers.signals import driver_post_save
from system.models import CarModel, CarColor
from users.models import User


class Driver(models.Model, BaseModelInterface):
    """ Driver model """
    DRIVER_STATUS_CHOICES = (
        (0, _("Offline")), (1, _("Available")), (2, _("Pending")),
        (3, _("Collecting passengers")), (4, _("Driving to pickup")), (5, _("Passenger onboard")),
        (6, _("En route")), (7, _("Completed")), (8, _("Cancelled")),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_licence_number = models.CharField(_("Driver licence number"), max_length=9, blank=True, null=True)

    status = models.IntegerField(default=0, choices=DRIVER_STATUS_CHOICES)

    approved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def send_to_staff_channel(self):
        bot = TeleBot(token=settings.TELEGRAM_BOT_TOKEN)
        username_text = f"(@{self.user.username})" if not self.user.username.startswith("user") else ""
        noty_text = f"<b>🧑‍✈️ Новый водитель</b>\n" \
                    f"<b>Имя:</b> {self.user.first_name} {username_text}\n" \
                    f"<b>Фамилия:</b> {self.user.last_name}\n" \
                    f"<b>Номер машины:</b> {self.get_car().car_number}\n\n" \
                    f"<b>Номер телефона:</b> +{self.user.phone}\n\n" \
                    f"#new_driver"
        bot.send_message(
            settings.TELEGRAM_STAFF_CHANNEL_ID,
            noty_text,
            parse_mode="HTML",
        )

    def get_car(self) -> "Car":
        return self.car_set.last()

    def __str__(self):
        return f"Driver {self.user}"

models.signals.post_save.connect(receiver=driver_post_save, sender=Driver)


class Car(models.Model, BaseModelInterface):
    """ Driver's car(s) model """
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car_number = models.CharField(max_length=8)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT, blank=True, null=True)
    color = models.ForeignKey(CarColor, on_delete=models.PROTECT, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model} {self.car_number}"

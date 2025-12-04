from django.db import models
from django.utils.translation import gettext_lazy as _

from birgo.classes.models import BaseModelInterface
from system.models import CarModel
from users.models import User


class Driver(models.Model, BaseModelInterface):
    """ Driver model """
    DRIVER_STATUS_CHOICES = (
        (0, _("Offline")), (1, _("Available")), (2, _("Pending")),
        (3, _("Collecting passengers")), (4, _("Driving to pickup")), (5, _("Passenger onboard")),
        (6, _("En route")), (7, _("Completed")), (8, _("Cancelled")),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_licence_number = models.CharField(max_length=9, blank=True, null=True)
    status = models.IntegerField(default=0, choices=DRIVER_STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Driver {self.user}"


class Car(models.Model, BaseModelInterface):
    """ Driver's car(s) model """
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car_number = models.CharField(max_length=8)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model} {self.car_number}"

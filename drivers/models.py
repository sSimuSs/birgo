from django.db import models

from birgo.classes.models import BaseModelInterface
from system.models import CarModel
from users.models import User


class Driver(models.Model, BaseModelInterface):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_licence_number = models.CharField(max_length=9, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Car(models.Model, BaseModelInterface):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car_number = models.CharField(max_length=8)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



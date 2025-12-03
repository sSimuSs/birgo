from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from birgo.classes.models import BaseModelInterface
from system.models import Region
from users.models import UserLocation


class TripRequest(models.Model, BaseModelInterface):
    """ Trip request model from the passengers, for drivers """
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    people_count = models.IntegerField(default=1)
    comments = models.TextField(blank=True, null=True)

    region_a = models.ForeignKey(Region, on_delete=models.SET_NULL,
                                 null=True,
                                 related_name="region_a")
    location_a = models.ForeignKey(UserLocation,
                                   on_delete=models.PROTECT,
                                   null=True, blank=True,
                                   related_name="location_a")

    region_b = models.ForeignKey(Region, on_delete=models.SET_NULL,
                                 null=True,
                                 related_name="region_b")
    location_b = models.ForeignKey(UserLocation,
                                   on_delete=models.PROTECT,
                                   null=True, blank=True,
                                   related_name="location_b")

    canceled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def cancel_trip_request(self):
        self.cancelled_at = timezone.now()
        self.save()


class Trip(models.Model, BaseModelInterface):
    """ Trip model """
    driver = models.ForeignKey("drivers.Driver", on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey("drivers.Car", on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def passengers(self) -> QuerySet["TripPassenger"]:
        """ Returns Passengers list queryset """
        return self.trippassenger_set.all()

    def passengers_count(self) -> int:
        """ Returns number of passengers """
        return self.passengers().count()


class TripPassenger(models.Model, BaseModelInterface):
    """ Trip passengers list item model"""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    passenger_user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    seat_number = models.IntegerField()

    trip_request = models.ForeignKey(TripRequest, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

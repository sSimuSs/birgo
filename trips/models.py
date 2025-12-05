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
    cost = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True, help_text="Total cost of the trip"
    )

    region_a = models.ForeignKey(Region, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name="region_a")
    location_a = models.ForeignKey(UserLocation,
                                   on_delete=models.PROTECT,
                                   null=True, blank=True,
                                   related_name="location_a")

    region_b = models.ForeignKey(Region, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name="region_b")
    location_b = models.ForeignKey(UserLocation,
                                   on_delete=models.PROTECT,
                                   null=True, blank=True,
                                   related_name="location_b")

    canceled_at = models.DateTimeField(blank=True, null=True)
    # user have submitted trip request and sent to drivers
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def cancel_trip_request(self):
        """ Method to cancel a trip request """
        self.canceled_at = timezone.now()
        self.save()

    def submit_trip_request(self) -> bool:
        """ Method to submit a trip request, it will be sent to drivers """
        result = False
        if self.people_count > 0:
            if (self.region_a or self.location_a) and (self.region_b or self.location_b):
                self.sent_at = timezone.now()
                self.save()
                result = True
        return result

    def views_count(self) -> int:
        """ Method to return the number of views by drivers """
        return self.triprequestview_set.count()

    def get_from_text(self) -> str | None:
        """ Method to get a trip request's "from" location/region name """
        text = None
        if self.region_a:
            text = self.region_a.get_tree_names()
        return text

    def get_to_text(self) -> str | None:
        """ Method to get a trip request's "to" location/region name """
        text = None
        if self.region_b:
            text = self.region_b.get_tree_names()
        return text

    def __str__(self):
        return f"TripRequest #{self.id} ({self.user})"


class TripRequestView(models.Model, BaseModelInterface):
    """ Trip request view model """
    trip_request = models.ForeignKey(TripRequest, on_delete=models.CASCADE)
    driver = models.ForeignKey("drivers.Driver", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    seat_number = models.IntegerField(blank=True, null=True)

    trip_request = models.ForeignKey(TripRequest, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

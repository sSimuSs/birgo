from django.db import models

from offers.constants import OFFER_STATUSES


class Offer(models.Model):
    lot = models.ForeignKey("lots.UserLot", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.FloatField()
    comment = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=OFFER_STATUSES, default=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.db import models

from offers.constants import OFFER_STATUSES
from wishr.classes.models import BaseModelInterface


class Offer(models.Model, BaseModelInterface):
    """ User lots' offer model class """
    lot = models.ForeignKey("lots.UserLot", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.FloatField()
    comment = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=OFFER_STATUSES, default=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_user_offers_count(self) -> int:
        """ Method for getting total number of user's offers for current lot """
        user_offers_count = self.lot.offer_set.filter(user=self.user).count()
        return user_offers_count

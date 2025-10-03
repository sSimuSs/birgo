from django.db import models
from django.utils import timezone
from django.utils.translation import get_language
from django.contrib.humanize.templatetags.humanize import naturalday

from offers.constants import OFFER_STATUSES


class Offer(models.Model):
    """ User lots' offer model class """
    lot = models.ForeignKey("lots.UserLot", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.FloatField()
    comment = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=OFFER_STATUSES, default=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def natural_created_at(self) -> str:
        """ Method for getting natural creation date of the offer """
        lang = get_language()
        today = timezone.now().date()
        created_at = timezone.make_naive(self.created_at)
        result = naturalday(created_at)
        if created_at.year == today.year:
            if lang == "en":
                result = naturalday(created_at, "N j")
            else:
                result = naturalday(created_at, "j N").lower()
        result += f" {str(created_at.strftime("%H:%M"))}"
        return result

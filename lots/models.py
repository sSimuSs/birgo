from django.conf import settings
from django.db import models

from lots.constants import USER_LOT_STATUSES


class UserLotCategory(models.Model):
    """ Lots' Category model """
    slug = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class UserLotCategoryTranslation(models.Model):
    """ Categories' Translation model """
    category = models.ForeignKey(UserLotCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=3, choices=settings.LANGUAGES)


class UserLot(models.Model):
    """ User's Lot model """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(UserLotCategory, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=5, choices=USER_LOT_STATUSES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

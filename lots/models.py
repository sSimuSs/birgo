from django.conf import settings
from django.db import models

from lots.constants import USER_LOT_STATUSES
from wishr.classes.models import BaseModelInterface


class UserLotCategory(models.Model):
    """ Lots' Category model """
    slug = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_name(self, user_lang: str) -> str:
        """
        Return the name of the category.
        If there is no the name text it will be returned the capitalized slug
        """
        name = self.slug.capitalize()
        print(user_lang)
        return name

    def __str__(self):
        return self.slug


class UserLotCategoryTranslation(models.Model):
    """ Categories' Translation model """
    category = models.ForeignKey(UserLotCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=3, choices=settings.LANGUAGES)


class UserLot(models.Model, BaseModelInterface):
    """ User's Lot model """
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(UserLotCategory, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(default=5, choices=USER_LOT_STATUSES)
    max_price = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_main_image_url(self) -> str:
        """ Method for getting lot's main image path (without host) """
        image_url = "/static/images/no-image.jpg"
        main_gallery_image = self.userlotgallery_set.filter(main=True).last()
        if main_gallery_image:
            image_url = f"{main_gallery_image.image.url}"
        return image_url

    def offers_count(self) -> int:
        """ Method for getting number of offers for current lot """
        return self.offer_set.filter(status=5).count()

    def get_cats(self, user_lang: str) -> list[dict]:
        """ Method for getting categories objects for current lot """
        hashtags = []
        if self.category:
            hashtags.append({
                "name": self.category.get_name(user_lang),
                "slug": self.category.slug,
            })
        return hashtags

    def __str__(self):
        return f"{self.title} #{self.id}"

class UserLotGallery(models.Model):
    """ Lots' Gallery model """
    lot = models.ForeignKey(UserLot, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="lots_images/")
    main = models.BooleanField(default=False)

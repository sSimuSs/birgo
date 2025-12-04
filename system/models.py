from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import get_language


class CarManufacturer(models.Model):
    """ Car manufacturer model """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """ CarModel model """
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(CarManufacturer, on_delete=models.CASCADE)
    seating_capacity = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.manufacturer}/{self.name}"


class CarColor(models.Model):
    """ CarColor model """
    name = models.CharField(max_length=255)
    hex_code = models.CharField(max_length=6, blank=True, null=True)

    def get_name(self, lang: str | None = None) -> str:
        name = self.name
        if lang:
            translation = self.carcolortranslation_set.filter(lang=lang).last()
            if translation:
                name = translation.name
        return name

    def __str__(self):
        return self.name


class CarColorTranslation(models.Model):
    """ CarColor's Translation model """
    car_color = models.ForeignKey(CarColor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=3, choices=settings.LANGUAGES)


class Region(models.Model):
    """ Region model """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    status = models.BooleanField(default=True)

    def sub_regions(self) -> QuerySet["Region"]:
        subregions = Region.objects.filter(parent=self, status=True)
        return subregions

    def sub_regions_count(self) -> int:
        return self.sub_regions().count()

    def get_name(self, lang: str | None = None) -> str:
        name = self.name

        if not lang:
            lang = get_language()

        translation = self.regiontranslation_set.filter(lang=lang).last()
        if translation:
            name = translation.name
        return name

    def get_tree_names(self, lang: str | None = None) -> str:
        if not lang:
            lang = get_language()

        name = self.get_name(lang)

        if self.parent:
            name = "{}, {}".format(self.parent.get_name(lang), name)

        return name

    def __str__(self):
        region_name = self.name
        if self.parent:
            region_name = f"{self.parent.name}, {self.name}"
        return region_name


class RegionTranslation(models.Model):
    """ Region's Translation model """
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=3, choices=settings.LANGUAGES)
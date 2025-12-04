from django.db import models
from django.db.models import QuerySet


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

    def __str__(self):
        region_name = self.name
        if self.parent:
            region_name = f"{self.parent.name}, {self.name}"
        return region_name
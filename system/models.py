from django.db import models


class CarManufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(CarManufacturer, on_delete=models.CASCADE)
    seating_capacity = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.manufacturer}/{self.name}"

from django.contrib import admin

from system.models import CarModel, CarManufacturer


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "manufacturer")
    search_fields = ("id", "name",)


@admin.register(CarManufacturer)
class CarManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name",)

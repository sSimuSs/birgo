from django.contrib import admin

from system.models import CarModel, CarManufacturer, Region, CarColor, CarColorTranslation, RegionTranslation


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    """ CarModel model admin"""
    list_display = ("id", "name", "manufacturer")
    search_fields = ("id", "name",)


@admin.register(CarManufacturer)
class CarManufacturerAdmin(admin.ModelAdmin):
    """ Car manufacturers model admin """
    list_display = ("id", "name")
    search_fields = ("id", "name",)


class RegionTranslationInline(admin.TabularInline):
    """ RegionTranslation inline for RegionAdmin """
    model = RegionTranslation
    extra = 0


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """ Region model admin """
    list_display = ("id", "name", "parent")
    search_fields = ("id", "name", "parent__name")
    list_filter = ("parent",)
    inlines = (RegionTranslationInline,)


class CarColorTranslationInline(admin.TabularInline):
    """ CarColorTranslation inline for CarColorAdmin """
    model = CarColorTranslation
    extra = 0

@admin.register(CarColor)
class CarColorAdmin(admin.ModelAdmin):
    """ CarColor model admin """
    list_display = ("id", "name", "hex_code")
    search_fields = ("id", "name", "hex_code")
    inlines = (CarColorTranslationInline,)

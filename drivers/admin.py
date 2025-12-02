from django.contrib import admin

from drivers.models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("id",)

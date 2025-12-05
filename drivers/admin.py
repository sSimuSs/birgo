from django.contrib import admin

from drivers.models import Driver, Car


class DriverCarInline(admin.TabularInline):
    """ Driver's cars inline for DriverAdmin """
    model = Car
    extra = 0


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """ Driver model admin class """
    list_display = ("id", "user", "status", "created_at", "approved_at")
    list_filter = ("created_at", "approved_at", "status")
    search_fields = ("id",)
    inlines = (DriverCarInline,)

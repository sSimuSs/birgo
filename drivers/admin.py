from django.contrib import admin

from drivers.models import Driver, Car


class DriverCarInline(admin.TabularInline):
    model = Car
    extra = 0


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """ Driver model admin class """
    list_display = ("id", "user")
    search_fields = ("id",)
    inlines = (DriverCarInline,)

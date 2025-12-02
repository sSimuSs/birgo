from django.contrib import admin

from trips.models import Trip, TripPassenger, TripRequest


@admin.register(TripRequest)
class TripRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    search_fields = ("id", "user__username", "user__first_name", "user__last_name")


class TripPassengerAdminInline(admin.TabularInline):
    model = TripPassenger
    extra = 0


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "driver", "passengers_count", "created_at")
    search_fields = ("id", "driver__driver_licence_number", "car__car_number")
    inlines = (TripPassengerAdminInline,)

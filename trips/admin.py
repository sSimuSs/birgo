from django.contrib import admin

from trips.models import Trip, TripPassenger, TripRequest, TripRequestView


@admin.register(TripRequest)
class TripRequestAdmin(admin.ModelAdmin):
    """ Trip request admin """
    list_display = ("id", "user", "created_at", "sent_at", "canceled_at")
    search_fields = ("id", "user__username", "user__first_name", "user__last_name")
    list_filter = ("created_at", )


class TripPassengerAdminInline(admin.TabularInline):
    """ Trip passengers list inline for TripAdmin """
    model = TripPassenger
    extra = 0


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """ Trip admin """
    list_display = ("id", "driver", "passengers_count", "created_at")
    search_fields = ("id", "driver__driver_licence_number", "car__car_number")
    list_filter = ("created_at", )
    inlines = (TripPassengerAdminInline,)


@admin.register(TripRequestView)
class TripRequestViewAdmin(admin.ModelAdmin):
    """ Trip request views admin """
    list_display = ("id", "trip_request", "driver", "created_at")
    search_fields = ("id", "trip_request_id", "driver_id", "driver__driver_licence_number", "trip_request__user__username")
    list_filter = ("created_at", )

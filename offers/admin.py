from django.contrib import admin

from offers.models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """ Admin for Offer model """
    list_display = ("id", "user", "lot", "created_at", "status")
    list_filter = ("status",)
    search_fields = ("id", "user__first_name", "user__last_name", "user__id", "lot__id", "lot__title")

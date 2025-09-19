from django.contrib import admin

from lots.models import UserLot, UserLotCategory, UserLotCategoryTranslation, UserLotGallery


class UserLotGalleryInline(admin.TabularInline):
    """ Gallery inline for UserLotAdmin """
    model = UserLotGallery
    extra = 0

@admin.register(UserLot)
class UserLotAdmin(admin.ModelAdmin):
    """ UserLot admin class """
    list_display = ("id", "user", "title", "max_price", "offers_count", "status", "created_at")
    search_fields = ("id", "slug", "title", "description", "user__first_name", "user__last_name")
    list_filter = ("status",)
    inlines = (UserLotGalleryInline,)

class UserLotCategoryTranslationInline(admin.TabularInline):
    """ Category translation inline for UserLotCategoryAdmin """
    model = UserLotCategoryTranslation
    extra = 0

@admin.register(UserLotCategory)
class UserLotCategoryAdmin(admin.ModelAdmin):
    """ Lots' category admin """
    list_display = ("id", "slug", "status")
    search_fields = ("id", "slug",)
    list_filter = ("status",)
    inlines = (UserLotCategoryTranslationInline,)

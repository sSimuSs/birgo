from django.contrib import admin

from lots.models import UserLot, UserLotCategory, UserLotCategoryTranslation, UserLotGallery


class UserLotGalleryInline(admin.TabularInline):
    model = UserLotGallery
    extra = 0

@admin.register(UserLot)
class UserLotAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "max_price", "status", "created_at")
    search_fields = ("id", "slug", "title", "description", "user__first_name", "user__last_name")
    list_filter = ("status",)
    inlines = (UserLotGalleryInline,)

class UserLotCategoryTranslationInline(admin.TabularInline):
    model = UserLotCategoryTranslation
    extra = 0

@admin.register(UserLotCategory)
class UserLotCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "status")
    search_fields = ("id", "slug",)
    list_filter = ("status",)
    inlines = (UserLotCategoryTranslationInline,)

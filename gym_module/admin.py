from django.contrib import admin

from gym_module.models import Gym, GymSession


# Register your models here.

class GymSessionInline(admin.StackedInline):
    model = GymSession
    extra = 0


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "contact_number", "created_at")
    search_fields = ("name", "owner__username", "location")
    list_filter = ("created_at",)

    inlines = [
        GymSessionInline
    ]

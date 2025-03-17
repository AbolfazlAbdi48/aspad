from django.contrib import admin

from gym_module.models import Gym


# Register your models here.
@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "contact_number", "created_at")
    search_fields = ("name", "owner__username", "location")
    list_filter = ("created_at",)

from django.contrib import admin
from core.models import Horse


# Register your models here.
@admin.register(Horse)
class HorseAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'breed', 'owner')
    search_fields = ('name', 'breed', 'owner__last_name', 'owner__first_name')

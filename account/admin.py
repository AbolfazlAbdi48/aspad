from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User, Skill, UserSkillProfile


# Register your models here.


class UserAdminModel(UserAdmin):
    pass


admin.site.register(User, UserAdminModel)


@admin.register(UserSkillProfile)
class UserSkillProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'offers__name')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass

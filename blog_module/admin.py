from django.contrib import admin

from blog_module.models import Article


# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'status')
    list_filter = ('created',)
    search_fields = ('title', 'summary', 'description')
    list_editable = ('status',)
    fieldsets = (
        ('اطلاعات مقاله', {'fields': ('title', 'summary', 'keywords', 'description')}),
        ('تصویر', {'fields': ('image',)}),
        ('وضعیت مشاهده', {'fields': ('publish_time', 'status')}),
    )

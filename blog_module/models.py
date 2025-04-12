from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from extentions.utils import jalali_converter_str


# Create your models here.
class Article(models.Model):
    """
    The Article main model,
    Many-To-Many relationship with Tag model.
    """

    class StatusChoices(models.TextChoices):
        published = 'p', 'منتشر شده'
        draft = 'd', 'چک نویس'

    title = models.CharField(max_length=155, verbose_name=_('عنوان'))
    summary = models.CharField(max_length=255, verbose_name=_('خلاصه'))
    description = models.TextField(verbose_name=_('توضیحات'))
    keywords = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('کلمات کلیدی'))
    image = models.ImageField(upload_to='blog/', verbose_name=_('تصویر اصلی'))
    status = models.CharField(max_length=5, choices=StatusChoices.choices, verbose_name=_('وضعیت انتشار'))
    publish_time = models.DateTimeField(default=timezone.now, verbose_name=_('زمان انتشار'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ ویرایش'))

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = '1. مقالات'
        ordering = ('-publish_time',)

    def get_thumbnail(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.image.url}'>")

    get_thumbnail.short_description = "تصویر"

    def get_absolute_url(self):
        return reverse('blog:blog-detail', args=[self.id, self.get_replaced_title()])

    def get_replaced_title(self):
        return self.title.replace(' ', '-')

    def published_jalali_str(self):
        return jalali_converter_str(self.publish_time)

    def __str__(self):
        return self.title

from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User


class Gym(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="gyms",
        verbose_name=_("مالک باشگاه")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("نام باشگاه")
    )
    description = models.TextField(
        verbose_name=_("توضیحات")
    )
    image = models.ImageField(
        upload_to="gyms/",
        verbose_name=_("تصویر باشگاه")
    )
    location = models.CharField(
        max_length=500,
        verbose_name=_("آدرس")
    )
    contact_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("شماره تماس")
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("ایمیل باشگاه")
    )
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("وب‌سایت")
    )
    opening_hours = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("ساعات کاری")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ثبت")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("آخرین بروزرسانی")
    )

    class Meta:
        verbose_name = _("باشگاه")
        verbose_name_plural = _("باشگاه‌ها")

    def __str__(self):
        return self.name

from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User


class Product(models.Model):
    name = models.CharField(_("نام محصول"), max_length=255)
    description = models.TextField(_("توضیحات"))
    price = models.DecimalField(_("قیمت"), max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(_("موجودی انبار"), default=0)
    image = models.ImageField(_("تصویر محصول"), upload_to="product_images/")
    created_at = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("آخرین بروزرسانی"), auto_now=True)

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

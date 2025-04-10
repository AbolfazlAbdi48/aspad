from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User


class Shop(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shops",
        verbose_name=_("مالک فروشگاه")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("نام فروشگاه")
    )
    description = models.TextField(
        verbose_name=_("توضیحات")
    )
    image = models.ImageField(
        upload_to="shops/",
        verbose_name=_("تصویر فروشگاه")
    )
    location = models.CharField(
        max_length=500,
        verbose_name=_("آدرس")
    )
    contact_number = models.CharField(
        max_length=20,
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
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ثبت")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("آخرین بروزرسانی")
    )

    class Meta:
        verbose_name = _("فروشگاه")
        verbose_name_plural = _("3. فروشگاه ها")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_("نام محصول"), max_length=255)
    description = models.TextField(_("توضیحات"))
    price = models.BigIntegerField(verbose_name=_('قیمت'), default=0)
    stock = models.PositiveIntegerField(_("موجودی انبار"), default=0)
    image = models.ImageField(_("تصویر محصول"), upload_to="product_images/")
    shop = models.ForeignKey(
        Shop, on_delete=models.PROTECT, null=True, related_name='products', verbose_name=_('فروشنده')
    )
    created_at = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("آخرین بروزرسانی"), auto_now=True)

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("1. محصولات")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='orders', verbose_name=_('کاربر')
    )
    address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('آدرس')
    )
    message = models.TextField(null=True, blank=True, verbose_name=_('پیام'))
    is_paid = models.BooleanField(default=False, verbose_name=_('وضعیت پرداخت'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ ویرایش'))

    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('2. سفارشات')
        ordering = ('-created',)

    def total_order_detail_price(self):
        total = 0
        for order_detail in self.order_details.all():
            total += order_detail.total_price()

        return total

    total_order_detail_price.short_description = 'مجموع سبد خرید'

    def __str__(self):
        return f"سفارش : {self.user} - شناسه : {self.id}"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_details', verbose_name=_('سفارش')
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name=_('محصول')
    )
    count = models.IntegerField(default=1, verbose_name=_('تعداد'))
    price = models.BigIntegerField(verbose_name=_('قیمت در زمان خرید'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ ویرایش'))

    class Meta:
        verbose_name = _('محصول در سفارش')
        verbose_name_plural = _('محصولات در سفارش')

    def total_price(self):
        return self.price * self.count

    def __str__(self):
        return f"{self.product} - {self.order}"

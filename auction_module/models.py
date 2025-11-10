from django.db import models

from account.models import User
from core.models import Horse
from django.utils.translation import gettext_lazy as _

from extentions.utils import jalali_converter_str


# Create your models here.
class Auction(models.Model):
    STATUS_CHOICES = [
        ('open', 'باز'),
        ('closed', 'بسته'),
        ('pending', 'در انتظار تایید'),
    ]

    HORSE_CATEGORY_CHOICES = [
        ('thoroughbred', 'اصیل انگلیسی'),
        ('arabian', 'اسب عربی'),
        ('quarter', 'کوارتر'),
        ('appaloosa', 'آپالوسا'),
        ('paint', 'پینت'),
        ('andalusian', 'آندالوسی'),
        ('friesian', 'فریزیان'),
        ('hanoverian', 'هانووری'),
        ('akhal_teke', 'آخال تکه'),
        ('mustang', 'موستانگ'),
        ('other', 'سایر'),
    ]

    PRICE_CATEGORY_CHOICES = [
        ('economy', 'اقتصادی (زیر ۱۰۰ میلیون)'),
        ('medium', 'متوسط (۱۰۰-۵۰۰ میلیون)'),
        ('premium', 'پریمیوم (۵۰۰ میلیون - ۱ میلیارد)'),
        ('luxury', 'لوکس (بالای ۱ میلیارد)'),
    ]

    horse = models.ForeignKey(Horse, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('اسب'))
    horse_name = models.CharField(null=True, max_length=255, verbose_name=_('نام اسب'))
    horse_age = models.IntegerField(null=True, verbose_name=_('سن'))
    horse_breed = models.CharField(null=True, max_length=255, verbose_name=_('نژاد اسب'))
    horse_summary = models.CharField(max_length=55, null=True, blank=True, verbose_name=_('خلاصه درباره اسب'))
    horse_description = models.TextField(null=True, verbose_name=_('درباره اسب'))
    horse_image = models.ImageField(null=True, upload_to='horses/', verbose_name=_('عکس اسب'))
    horse_video = models.FileField(null=True, blank=True, upload_to='horses/', verbose_name=_('ویدئو اسب'))
    horse_doc = models.FileField(null=True, blank=True, upload_to='horses/', verbose_name=_('مدارک اسب'))
    horse_category = models.CharField(
        max_length=20,
        choices=HORSE_CATEGORY_CHOICES,
        null=True,
        blank=True,
        verbose_name="نژاد اسب"
    )
    price_category = models.CharField(
        max_length=20,
        choices=PRICE_CATEGORY_CHOICES,
        null=True,
        blank=True,
        verbose_name="محدوده قیمت"
    )
    start_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_('حداقل مبلغ مزایده'))
    start_time = models.DateTimeField(verbose_name=_('شروع مزایده'))
    end_time = models.DateTimeField(verbose_name=_('پایان مزایده'))
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   verbose_name=_('ساخته شده توسط'))
    status = models.CharField(max_length=10, null=True, blank=True, choices=STATUS_CHOICES, default='open',
                              verbose_name=_('وضعیت مزایده'))

    class Meta:
        verbose_name_plural = '1. مزایده ها'
        verbose_name = 'مزایده'
        ordering = ('-start_time',)

    def get_start_time_jalali(self):
        return jalali_converter_str(self.start_time)

    get_start_time_jalali.short_description = 'شروع مزایده'

    def get_end_time_jalali(self):
        return jalali_converter_str(self.end_time)

    get_end_time_jalali.short_description = 'پایان مزایده'

    def get_start_price(self):
        return f"{self.start_price:,}"

    get_start_price.short_description = 'حداقل مبلغ مزایده'

    def __str__(self):
        return f"مزایده برای {self.horse_name}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids", verbose_name=_('مزایده'))
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('پیشنهاد توسط'))
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_('قیمت پیشنهادی'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('زمان ثبت'))
    is_winner = models.BooleanField(default=False, verbose_name=_('برنده مزایده'))

    class Meta:
        verbose_name_plural = '2. پیشنهاد ها'
        verbose_name = 'پیشنهاد'
        ordering = ("-amount",)

    def get_created_jalali(self):
        return jalali_converter_str(self.created)

    get_created_jalali.short_description = 'زمان ثبت پیشنهاد'

    def get_amount(self):
        return f"{self.amount:,}"

    get_amount.short_description = 'قیمت پیشنهادی'

    def __str__(self):
        return f"توسط {self.bidder.get_full_name()}"

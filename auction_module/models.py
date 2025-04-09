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

    horse = models.ForeignKey(Horse, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('اسب'))
    horse_name = models.CharField(max_length=255,  verbose_name=_('نام'))
    horse_age = models.IntegerField( verbose_name=_('سن'))
    horse_breed = models.CharField( max_length=255, verbose_name=_('نژاد'))
    horse_description = models.TextField( verbose_name=_('توضیحات'))
    horse_image = models.ImageField( upload_to='horses/', verbose_name=_('عکس'))
    start_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_('حذاقل پیشنهاد'))
    start_time = models.DateTimeField(verbose_name=_('شروع مزایده'))
    end_time = models.DateTimeField(verbose_name=_('پایان مزایده'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('ساخته شده توسط'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open', verbose_name=_('وضعیت مزایده'))

    class Meta:
        verbose_name_plural = '1. مزایده ها'
        verbose_name = 'مزایده'

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

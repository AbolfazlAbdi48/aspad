from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User
from core.models import Horse
from extentions.utils import jalali_converter_str


# Create your models here.
class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    experience_years = models.IntegerField(verbose_name=_("Years of Experience"))
    about = models.TextField(verbose_name=_("Specialization"))
    verified = models.BooleanField(default=False, verbose_name=_("Verified"))
    blocked = models.BooleanField(default=False, verbose_name=_("Blocked"))

    class Meta:
        verbose_name = 'کارشناس'
        verbose_name_plural = '1. کارشناس ها'

    def __str__(self):
        return f"{self.user.username} - کارشناس"


class HorseEvaluationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('rejected', _('Rejected')),
    ]

    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, verbose_name=_("اسب"))
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Requested By"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name=_("Status")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = 'درخواست کارشناسی'
        verbose_name_plural = '2. درخواست های کارشناسی'

    def get_created_jalali(self):
        return jalali_converter_str(self.created_at)

    get_created_jalali.short_description = 'زمان ایجاد درخواست'

    def __str__(self):
        return f"کارشناسی {self.horse.name}"


class HorseEvaluationReport(models.Model):
    evaluation_request = models.ForeignKey(
        HorseEvaluationRequest, on_delete=models.CASCADE, verbose_name=_("Evaluation Request")
    )
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, verbose_name=_("Expert"))
    report_text = models.TextField(verbose_name=_("Report Text"))
    authenticity_score = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Authenticity Score")
    )
    health_score = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Health Score")
    )
    speed_score = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Speed Score")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = 'گزارش کارشناسی'
        verbose_name_plural = '3. گزارش های کارشناسی'

    def get_created_jalali(self):
        return jalali_converter_str(self.created_at)

    get_created_jalali.short_description = 'زمان پاسخ کارشناس'

    def __str__(self):
        return f"گزارش {self.expert.user.username} برای {self.evaluation_request.horse.name}"

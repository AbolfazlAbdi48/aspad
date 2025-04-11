from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    """
    Customize User's Model.
    """
    pass


class Skill(models.Model):
    name = models.CharField(max_length=255, verbose_name='مهارت')

    class Meta:
        verbose_name_plural = _('مهارت ها')
        verbose_name = _('مهارت')

    def __str__(self):
        return self.name


class UserSkillProfile(models.Model):
    ROLE_CHOICES = [
        ('coach', 'مربی'),
        ('vet', 'دامپزشک'),
        ('gym_owner', 'باشگاه‌دار'),
        ('shop_owner', 'فروشگاه‌دار'),
        ('user', 'کاربر عادی'),
        ('expert', 'کارشناس'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name=_("نقش کاربر")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='skill_profile')
    offers = models.ManyToManyField(Skill, related_name='offered_by', verbose_name=_('عرضه‌ها'))
    demands = models.ManyToManyField(Skill, related_name='demanded_by', verbose_name=_('تقاضاها'))

    class Meta:
        verbose_name_plural = _('پروفایل ها')
        verbose_name = _('پروفایل')

    def __str__(self):
        return f"پروفایل مهارتی {self.user.username}"

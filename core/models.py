from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User


# Create your models here.
class Horse(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('نام'))
    age = models.IntegerField(verbose_name=_('سن'))
    breed = models.CharField(max_length=255, verbose_name=_('نژاد'))
    description = models.TextField(verbose_name=_('توضیحات'))
    image = models.ImageField(upload_to='horses/', verbose_name=_('عکس'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('مالک'))

    class Meta:
        verbose_name_plural = '1. اسب ها'
        verbose_name = 'اسب'

    def __str__(self):
        return f"اسب: {self.name}"

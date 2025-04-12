import re
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from auction_module.models import Auction
from .models import UserSkillProfile, Skill


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': '09xxxxxxxxx'
        }),
        help_text='شماره موبایل با 09 شروع شود.',
        label='شماره موبایل',
        min_length=11,
        max_length=11
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        regex = r"^[0-9]{2,}[0-9]$"
        subst = ""
        result = re.sub(regex, subst, phone_number, 0, re.MULTILINE)
        if len(phone_number) != 11 and not result:
            raise forms.ValidationError('لطفا شماره موبایل را به درستی وارد کنید.')
        return phone_number


class PasswordVerifyForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'رمزعبور'
        }),
        label='رمزعبور'
    )


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'نام'
        }),
        label='نام'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'نام خانوادگی'
        }),
        label='نام خانوادگی'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'رمزعبور'
        }),
        help_text=password_validation.password_validators_help_text_html(),
        label='رمزعبور'
    )
    user_type = forms.ChoiceField(
        choices=UserSkillProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='نقش شما در اسپاد چیست؟'
    )

    offers = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='چه خدمات و مهارت هایی ارائه میدهید؟',
        required=True
    )

    demands = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='به چه خدماتی نیاز دارید؟',
        required=True
    )


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['horse_name', 'horse_age', 'horse_breed', 'horse_description',
                  'horse_image', 'start_price', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
        }
        labels = {
            'start_time': _('زمان شروع مزایده'),
            'end_time': _('زمان پایان مزایده'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control'

import re
from django import forms
from django.contrib.auth import password_validation


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

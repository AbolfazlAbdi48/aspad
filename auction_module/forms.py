from django import forms
from .models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(
                attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, auction=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.auction = auction

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if not self.auction:
            raise forms.ValidationError("مزایده‌ای برای این پیشنهاد یافت نشد.")

        if amount <= self.auction.start_price:
            raise forms.ValidationError("پیشنهاد شما باید بیشتر از قیمت پایه باشد.")

        return amount

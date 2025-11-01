import django_filters
from .models import Auction


class AuctionFilter(django_filters.FilterSet):
    horse_name = django_filters.CharFilter(
        field_name='horse_name',
        lookup_expr='icontains',
        label='نام اسب'
    )

    horse_category = django_filters.ChoiceFilter(
        choices=Auction.HORSE_CATEGORY_CHOICES,
        label='دسته‌بندی اسب'
    )

    price_category = django_filters.ChoiceFilter(
        choices=Auction.PRICE_CATEGORY_CHOICES,
        label='دسته‌بندی قیمت'
    )

    class Meta:
        model = Auction
        fields = ['horse_name', 'horse_category', 'price_category']

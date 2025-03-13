from django.contrib import admin

from auction_module.models import Auction, Bid


# Register your models here.
@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_start_price', 'get_start_time_jalali', 'status')
    list_editable = ('status',)
    list_filter = ('start_time', 'end_time')
    search_fields = ('created_by__first_name', 'created_by__last_name', 'horse__name')


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'bidder', 'get_amount', 'get_created_jalali', 'is_winner')
    list_editable = ('is_winner',)
    search_fields = ('auction__horse__name', 'bidder__first_name', 'bidder__last_name')

from django.shortcuts import render

from auction_module.models import Auction


# Create your views here.
def home(request):
    auctions = Auction.objects.filter()[:4]

    context = {
        "auctions": auctions
    }
    return render(request, "core/home.html", context)

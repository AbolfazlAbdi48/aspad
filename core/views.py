from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from auction_module.models import Auction
from blog_module.models import Article
from gym_module.models import Gym
from shop_module.models import Shop, Product


# Create your views here.
def home(request):
    auctions = Auction.objects.filter()[:4]
    blog = Article.objects.filter(status='p', publish_time__lte=timezone.now())[:3]

    context = {
        "auctions": auctions,
        "blog": blog
    }
    return render(request, "core/home.html", context)


def search_view(request):
    search = request.GET.get("search")

    if not search:
        search = "None"

    auction_search = Auction.objects.filter(
        Q(horse_name__icontains=search) |
        Q(horse_description__icontains=search) |
        Q(horse_breed__icontains=search)
    )
    gym_search = Gym.objects.filter(
        Q(owner__first_name__icontains=search) |
        Q(owner__last_name__icontains=search) |
        Q(name__icontains=search) |
        Q(location__icontains=search) |
        Q(description__icontains=search)
    )
    shop_search = Shop.objects.filter(
        Q(owner__first_name__icontains=search) |
        Q(owner__last_name__icontains=search) |
        Q(name__icontains=search) |
        Q(location__icontains=search) |
        Q(description__icontains=search)
    )
    product_search = Product.objects.filter(
        Q(name__icontains=search) |
        Q(description__icontains=search)
    )
    # TODO: Trainer search

    context = {
        "search": search,
        "auction_search": auction_search,
        "gym_search": gym_search,
        "shop_search": shop_search,
        "product_search": product_search,
    }
    return render(request, "core/search.html", context)

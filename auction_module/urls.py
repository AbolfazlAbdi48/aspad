from django.urls import path
from .views import (
    AuctionDetailView,
    BidCreateView,
    AuctionListView
)

app_name = "auction"
urlpatterns = [
    path("", AuctionListView.as_view(), name="auction-list"),
    path("<int:pk>/", AuctionDetailView.as_view(), name="auction-detail"),
    path("<int:pk>/bid", BidCreateView.as_view(), name="auction-bid"),
]

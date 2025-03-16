from django.urls import path
from .views import (
    AuctionDetailView,
    BidCreateView
)

app_name = "auction"
urlpatterns = [
    path("<int:pk>/", AuctionDetailView.as_view(), name="auction-detail"),
    path("<int:pk>/bid", BidCreateView.as_view(), name="auction-bid"),
]

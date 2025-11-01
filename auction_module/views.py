from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, CreateView, ListView
from django.urls import reverse

from auction_module.filters import AuctionFilter
from auction_module.forms import BidForm
from auction_module.models import Auction, Bid


# Create your views here.
class AuctionListView(ListView):
    model = Auction
    template_name = "auction/auction_list.html"

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-start_time')
        self.filterset = AuctionFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class AuctionDetailView(DetailView):
    model = Auction
    template_name = "auction/auction_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auction = self.get_object()
        has_bid = False
        if self.request.user.is_authenticated:
            has_bid = auction.bids.filter(bidder=self.request.user).exists()
        context["user_has_bid"] = has_bid
        context["now"] = timezone.now()
        return context


class BidCreateView(LoginRequiredMixin, CreateView):
    model = Bid
    form_class = BidForm
    template_name = "auction/bid_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["auction"] = get_object_or_404(Auction, pk=self.kwargs["pk"])
        return kwargs

    def form_valid(self, form):
        bid = form.save(commit=False)
        bid.auction = get_object_or_404(Auction, pk=self.kwargs["pk"])
        bid.bidder = self.request.user
        bid.save()
        messages.success(self.request, "پیشنهاد شما با موفقیت ثبت شد")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("auction:auction-detail", kwargs={"pk": self.kwargs["pk"]})

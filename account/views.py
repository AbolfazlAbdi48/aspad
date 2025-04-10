from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from account.forms import PhoneNumberForm, RegisterForm, PasswordVerifyForm, AuctionForm
from account.models import User
from auction_module.models import Auction
from evaluation_module.models import HorseEvaluationRequest
from extentions.utils import get_client_ip


# Create your views here.
def login_view(request):
    form = PhoneNumberForm(request.POST or None)
    ip = get_client_ip(request)
    next_url = request.GET.get('next')

    if next_url:
        cache.set(f"{ip}-for-next-url", next_url, 500)

    if form.is_valid():
        phone_number = form.cleaned_data.get('phone_number')
        user_exist: bool = User.objects.filter(username=phone_number).exists()

        ip = get_client_ip(request)
        cache.set(f"{ip}-for-authentication", phone_number, 1000)

        if user_exist:
            return redirect("account:verify-password")
        else:
            User.objects.create_user(username=phone_number)
            return redirect("account:login-complete")

    context = {
        'form': form
    }
    return render(request, 'account/phone_auth.html', context)


def verify_pass_view(request):
    form = PasswordVerifyForm(request.POST or None)

    ip = get_client_ip(request)
    phone = cache.get(f"{ip}-for-authentication")
    next_url = cache.get(f"{ip}-for-next-url")

    if phone is None:
        raise Http404

    user = get_object_or_404(User, username=phone)

    if form.is_valid():
        password = form.cleaned_data.get('password')

        authenticated_user = authenticate(request, username=user.username, password=password)

        if authenticated_user:
            cache.delete(f"{ip}-for-authentication")
            login(request, user=authenticated_user)
            messages.success(request, "به اسپاد خوش آمدید!")

            if next_url:
                return redirect(next_url)
            return redirect('core:home')
        else:
            messages.error(request, 'رمز عبور اشتباه وارد شده است.')

    context = {
        'form': form,
        'phone': phone
    }
    return render(request, 'account/verify_otp.html', context)


def complete_register_view(request):
    form = RegisterForm(request.POST or None)
    ip = get_client_ip(request)
    next_url = cache.get(f"{ip}-for-next-url")
    phone = cache.get(f"{ip}-for-authentication")

    try:
        user = User.objects.get(username=phone)
    except User.DoesNotExist:
        raise Http404

    if form.is_valid():
        cd = form.cleaned_data  # cleaned data

        user.first_name = cd.get('first_name')
        user.last_name = cd.get('last_name')
        user.set_password(cd.get('password'))
        user.save()

        login(request, user)
        messages.success(request, message="به اسپاد خوش آمدید!")
        cache.delete(f"{ip}-for-authentication")
        if next_url:
            return redirect(next_url)
        return redirect('core:home')

    context = {
        'form': form
    }
    return render(request, 'account/complete_register.html', context)


def custom_logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def profile_view(request):
    return render(request, "account/profile.html")


class EvaluationRequestListView(LoginRequiredMixin, ListView):
    model = HorseEvaluationRequest
    template_name = 'account/evaluation_request_list.html'

    def get_queryset(self):
        return HorseEvaluationRequest.objects.filter(requested_by=self.request.user).order_by("-created_at")


class EvaluationRequestDetailView(LoginRequiredMixin, DetailView):
    model = HorseEvaluationRequest
    template_name = 'account/evaluation_request_detail.html'


class EvaluationRequestCreateView(LoginRequiredMixin, CreateView):
    model = HorseEvaluationRequest
    fields = ['horse_name', 'horse_age', 'horse_breed', 'horse_image', 'comment']
    template_name = 'account/evaluation_request_create.html'
    success_url = reverse_lazy('account:profile-evaluation-requests')

    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        return super().form_valid(form)


class UserAuctionListView(LoginRequiredMixin, ListView):
    model = Auction
    template_name = 'account/user_auction_list.html'

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)


class UserAuctionCreateView(LoginRequiredMixin, CreateView):
    model = Auction
    form_class = AuctionForm
    template_name = 'account/user_auction_form.html'
    success_url = reverse_lazy('account:profile-auction-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UserAuctionUpdateView(LoginRequiredMixin, UpdateView):
    model = Auction
    form_class = AuctionForm
    template_name = 'account/user_auction_form.html'
    success_url = reverse_lazy('account:profile-auction-list')

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)

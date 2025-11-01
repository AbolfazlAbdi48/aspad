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
from account.models import User, UserSkillProfile, LoginSession
from auction_module.models import Auction
from evaluation_module.models import HorseEvaluationRequest
from extentions.data_matching import find_matches_for_user
from extentions.utils import get_client_ip
from gym_module.forms import GymForm, GymSessionForm
from gym_module.models import Gym, GymSession


# Create your views here.
def login_view(request):
    form = PhoneNumberForm(request.POST or None)
    ip = get_client_ip(request)
    next_url = request.GET.get('next')

    if form.is_valid():
        phone_number = form.cleaned_data.get('phone_number')
        user_exist = User.objects.filter(username=phone_number).first()

        LoginSession.objects.filter(ip_address=ip).delete()

        LoginSession.objects.create(
            ip_address=ip,
            phone_number=phone_number,
            next_url=next_url
        )

        if user_exist:
            if user_exist.is_active:
                return redirect("account:verify-password")
            return redirect("account:login-complete")
        else:
            User.objects.create_user(username=phone_number, is_active=False)
            return redirect("account:login-complete")

    context = {
        'form': form
    }
    return render(request, 'account/phone_auth.html', context)


def verify_pass_view(request):
    form = PasswordVerifyForm(request.POST or None)
    ip = get_client_ip(request)

    session = LoginSession.objects.filter(ip_address=ip).first()
    if not session:
        raise Http404

    phone = session.phone_number
    next_url = session.next_url
    user = get_object_or_404(User, username=phone)

    if form.is_valid():
        password = form.cleaned_data.get('password')
        authenticated_user = authenticate(request, username=user.username, password=password)

        if authenticated_user:
            login(request, user=authenticated_user)
            messages.success(request, "به اسپاد خوش آمدید!")

            session.delete()

            if next_url:
                return redirect(next_url)
            return redirect('account:profile-match')
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

    session = LoginSession.objects.filter(ip_address=ip).first()
    if not session:
        raise Http404

    phone = session.phone_number
    next_url = session.next_url

    try:
        user = User.objects.get(username=phone)
    except User.DoesNotExist:
        raise Http404

    if form.is_valid():
        cd = form.cleaned_data

        user.first_name = cd.get('first_name')
        user.last_name = cd.get('last_name')
        user.set_password(cd.get('password'))
        user.is_active = True
        user.save()

        profile = UserSkillProfile.objects.create(
            user=user,
            role=form.cleaned_data.get('user_type')
        )
        profile.offers.set(form.cleaned_data.get('offers'))
        profile.demands.set(form.cleaned_data.get('demands'))

        login(request, user)
        messages.success(request, message="به اسپاد خوش آمدید!")

        # حذف داده بعد از ثبت‌نام کامل
        session.delete()

        if next_url:
            return redirect(next_url)
        return redirect('account:profile-match')

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


@login_required()
def profile_match_view(request):
    """
    data matching view.
    """
    matches = find_matches_for_user(request.user)
    context = {
        'object_list': matches['offers_for_user'],
        'matches': matches
    }
    return render(request, "account/profile_match.html", context)


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
    fields = ['horse_name', 'horse_age', 'horse_breed', 'horse_image', 'horse_video', 'horse_doc_first',
              'horse_doc_second', 'horse_doc_third', 'comment']
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


@login_required
def gym_profile_view(request):
    user = request.user
    if user.skill_profile.role != 'gym_owner':
        return redirect('account:profile')

    gym = Gym.objects.filter(owner=user).first()

    if request.method == 'POST':
        form = GymForm(request.POST, request.FILES, instance=gym)
        if form.is_valid():
            gym = form.save(commit=False)
            gym.owner = user
            gym.save()
            return redirect('account:profile')
    else:
        form = GymForm(instance=gym)

    context = {
        'form': form,
        'is_edit': bool(gym)
    }
    return render(request, 'account/gym_profile_edit.html', context)


def gym_reserve_list_view(request):
    gym = get_object_or_404(Gym, owner=request.user)

    context = {
        'reserves': gym.sessions.all()
    }
    return render(request, "account/gym_reserves.html", context)


@login_required
def create_gym_session_view(request):
    user = request.user
    if user.skill_profile.role != 'gym_owner':
        return redirect('account:profile')

    gym = Gym.objects.filter(owner=user).first()
    if not gym:
        return redirect('account:profile-gym-form')

    if request.method == 'POST':
        form = GymSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.gym = gym
            session.save()
            messages.success(request, "سانس با موفقیت ایجاد شد.")
            return redirect('account:profile')
    else:
        form = GymSessionForm()

    context = {
        'form': form
    }
    return render(request, 'account/gym_create_session.html', context)

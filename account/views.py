from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import PhoneNumberForm, RegisterForm, PasswordVerifyForm
from account.models import User
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
        # TODO: cache next url

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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from gym_module.models import Gym, GymSession


# Create your views here.
class GymListView(ListView):
    model = Gym
    template_name = "gym/gym_list.html"


class GymDetailView(DetailView):
    model = Gym
    template_name = "gym/gym_detail.html"


@login_required
def reserve_session_view(request, pk):
    session = get_object_or_404(GymSession, id=pk)
    reserved = False
    if request.user in session.reserved_by.all():
        reserved = True

    if request.method == 'POST':
        if request.user in session.reserved_by.all():
            messages.warning(request, "شما قبلا این سانس را رزرو کرده اید. به زودی با شما تماس میگیریم.")
        else:
            session.reserved_by.add(request.user)
            messages.success(request, "رزرو شما با موفقیت انجام شد. به زودی با شما تماس میگیریم.")
        return redirect('gym:gym-detail', pk=session.gym.pk)

    context = {
        'session': session,
        'reserved': reserved
    }
    return render(request, 'gym/session_reserve_confirm.html', context)

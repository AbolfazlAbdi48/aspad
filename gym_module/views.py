from django.shortcuts import render
from django.views.generic import ListView, DetailView

from gym_module.models import Gym


# Create your views here.
class GymListView(ListView):
    model = Gym
    template_name = "gym/gym_list.html"


class GymDetailView(DetailView):
    model = Gym
    template_name = "gym/gym_detail.html"

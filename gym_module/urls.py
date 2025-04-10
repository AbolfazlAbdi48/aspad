from django.urls import path
from .views import GymListView, GymDetailView, reserve_session_view

app_name = "gym"
urlpatterns = [
    path("", GymListView.as_view(), name="gym-list"),
    path("<int:pk>/", GymDetailView.as_view(), name="gym-detail"),
    path('session/<int:pk>/', reserve_session_view, name='reserve-session'),

]

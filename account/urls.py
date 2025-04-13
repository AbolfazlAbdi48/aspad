from django.urls import path
from .views import (
    login_view,
    complete_register_view,
    verify_pass_view,
    profile_view,
    custom_logout_view,
    EvaluationRequestListView,
    EvaluationRequestDetailView,
    EvaluationRequestCreateView,
    UserAuctionListView,
    UserAuctionCreateView,
    UserAuctionUpdateView,
    profile_match_view,
    gym_profile_view, gym_reserve_list_view, create_gym_session_view,
)

app_name = "account"
urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path("profile/match/", profile_match_view, name="profile-match"),
    path("profile/evaluations/", EvaluationRequestListView.as_view(), name="profile-evaluation-requests"),
    path("profile/evaluations/create", EvaluationRequestCreateView.as_view(), name="profile-evaluation-Create"),
    path("profile/evaluations/<int:pk>", EvaluationRequestDetailView.as_view(), name="profile-evaluation-detail"),
    path("profile/auctions/", UserAuctionListView.as_view(), name="profile-auction-list"),
    path("profile/auctions/create", UserAuctionCreateView.as_view(), name="profile-auction-create"),
    path("profile/auctions/update/<int:pk>", UserAuctionUpdateView.as_view(), name="profile-auction-update"),
    path("profile/gym/form", gym_profile_view, name="profile-gym-form"),
    path("profile/gym/reserves", gym_reserve_list_view, name="profile-gym-reserves"),
    path("profile/gym/session", create_gym_session_view, name="profile-gym-session-create"),

    path("logout/", custom_logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("login/complete/", complete_register_view, name="login-complete"),
    path("login/pswd/", verify_pass_view, name="verify-password"),
]

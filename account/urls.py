from django.urls import path
from .views import (
    login_view,
    complete_register_view,
    verify_pass_view,
    profile_view,
    EvaluationRequestListView,
    EvaluationRequestDetailView,
    EvaluationRequestCreateView
)

app_name = "account"
urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path("profile/evaluations/", EvaluationRequestListView.as_view(), name="profile-evaluation-requests"),
    path("profile/evaluations/create", EvaluationRequestCreateView.as_view(), name="profile-evaluation-Create"),
    path("profile/evaluations/<int:pk>", EvaluationRequestDetailView.as_view(), name="profile-evaluation-detail"),

    path("login/", login_view, name="login"),
    path("login/complete/", complete_register_view, name="login-complete"),
    path("login/pswd/", verify_pass_view, name="verify-password"),
]

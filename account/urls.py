from django.urls import path
from .views import login_view, complete_register_view, verify_pass_view

app_name = "account"
urlpatterns = [
    path("login/", login_view, name="login"),
    path("login/complete/", complete_register_view, name="login-complete"),
    path("login/pswd/", verify_pass_view, name="verify-password"),
]

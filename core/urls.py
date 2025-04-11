from django.urls import path

from core.views import home, search_view

app_name = "core"
urlpatterns = [
    path("", home, name="home"),
    path("search/", search_view, name="search-view"),
]

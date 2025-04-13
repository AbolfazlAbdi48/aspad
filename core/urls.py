from django.urls import path

from core.views import home, search_view, CoachListView

app_name = "core"
urlpatterns = [
    path("", home, name="home"),
    path("search/", search_view, name="search-view"),
    path("coach/", CoachListView.as_view(), name="coach-List"),
]

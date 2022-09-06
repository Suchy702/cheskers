from django.urls import include, path
from . import views

urlpatterns = [
    path("matchmake/", views.MatchmakeView.as_view()),
]

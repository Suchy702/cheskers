from django.urls import path
from . import views

urlpatterns = [
    path("matchmake/", views.MatchmakeView.as_view()),
]

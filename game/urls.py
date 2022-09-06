from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path("matchmake/", views.MatchmakeView.as_view()),
    path("add_to_waiting_list/", views.MatchmakingQueueView.as_view()),
    path("try_to_pair/", views.PairMakerView.as_view()),
    path("board/<str:session_id>", views.GameSessionView.as_view(), name="game_session")
]

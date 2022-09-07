from django.http import HttpResponse
from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path("matchmake/", views.MatchmakeView.as_view(), name="matchmake"),
    path("add_to_queue/", views.MatchmakingQueueView.as_view()),
    path("try_to_pair/", views.PairMakerView.as_view()),
    path("board/", lambda: HttpResponse(status=404), name="game_session_prefix"),
    path("board/<str:session_id>", views.GameSessionView.as_view(), name="game_session")
]


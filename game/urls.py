from django.http import HttpResponse
from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path("matchmake/", views.MatchmakeView.as_view(), name="matchmake"),
    path("add_to_queue/", views.MatchmakingQueueView.as_view()),
    path("try_to_pair/", views.PairMakerView.as_view()),
    path("board/", lambda: HttpResponse(status=404), name="game_session_prefix"),
    path("board/<str:session_id>", views.GameSessionView.as_view(), name="game_session"),
    path("guest_login/", views.GuestLoginView.as_view(), name='guest_login'),
    path("result/<str:session_url>", views.ResultView.as_view(), name='result'),
    path("ranking/", views.RankingView.as_view(), name='ranking'),
    path("create_room/", views.CreateRoomView.as_view(), name='create_room'),
    path("join_room/", views.JoinRoomView.as_view(), name='join_room')
]


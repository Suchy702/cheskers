from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

from .models import GameSessionModel, PlayerModel

def enforce_game_session(get_response):

    def middleware(request):
        if not request.META['PATH_INFO'].startswith(reverse('game:game_session_prefix')) and PlayerModel.get_client_from_request(request) is not None:
            ongoing_session = GameSessionModel.get_ongoing_session_url(PlayerModel.get_client_from_request(request))
            if ongoing_session is not None:
                return HttpResponseRedirect(reverse('game:game_session', args=[ongoing_session]))

        response = get_response(request)

        return response

    return middleware
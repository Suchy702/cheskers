from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import MatchmakingQueueModel, GameSessionModel

def enforce_game_session(get_response):

    def middleware(request):
        if not request.META['PATH_INFO'].startswith('/game/board') and 'id' in request.session:
            ongoing_session = GameSessionModel.get_ongoing_session_id(request.session['id'])
            if ongoing_session is not None:
                return HttpResponseRedirect(reverse('game:game_session', args=[ongoing_session]))

        response = get_response(request)

        return response

    return middleware
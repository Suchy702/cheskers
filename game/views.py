import random
import datetime

from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from .mixins import IDRequiredMixin
from .models import MatchmakingQueueModel, GameSessionModel, PlayerModel


class GameBaseView(IDRequiredMixin, View):
    pass


class MatchmakeView(GameBaseView, TemplateView):
    template_name = "game/matchmake.html"


class MatchmakingQueueView(GameBaseView):
    @transaction.atomic
    def post(self, request):
        client = PlayerModel.get_client(request)
        if MatchmakingQueueModel.is_in_queue(client):
            record = PlayerModel.objects_get(MatchmakingQueueModel.objects, client)
        else:
            record = MatchmakingQueueModel.create(client)

        record.save()
        return HttpResponse(status=200)


class PairMakerView(GameBaseView):
    def post(self, request):
        client = PlayerModel.get_client(request)
        if not MatchmakingQueueModel.is_in_queue(client):
            raise Http404("Error in matchmaking algorithm")

        current_client = PlayerModel.objects_get(MatchmakingQueueModel.objects, client)
        current_client.save()
        MatchmakingQueueModel.clean_queue()

        with transaction.atomic():
            current_client.delete()
            other_client = MatchmakingQueueModel.objects.order_by('last_updated').first()

            if other_client is None:
                raise ObjectDoesNotExist()

            other_client.delete()
            game_session = GameSessionModel.create(current_client.client_id, other_client.client_id)
            game_session.save()

        return HttpResponseRedirect(reverse('game:game_session', args=[game_session.session_id]))


class GameSessionView(GameBaseView, TemplateView):
    template_name = "game/board.html"

    def get(self, request, session_id):
        game_session = GameSessionModel.get_ongoing_session_by_url(session_id)

        if game_session is not None:
            client = PlayerModel.get_client(request)
            if self.is_authorized(client, game_session):
                return super().get(request)

        return HttpResponseRedirect(reverse('game:matchmake'))

    def is_authorized(self, client, game_session):
        return client == game_session.white_player.get_id() \
            or client == game_session.black_player.get_id()

class GuestLoginView(View):
    def get(self, request):
        PlayerModel.create_guest(request)
        return HttpResponseRedirect(reverse('game:matchmake'))
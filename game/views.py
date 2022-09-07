import random
import datetime

from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import MatchmakingQueueModel, GameSessionModel

class GameBaseView(LoginRequiredMixin, View):
    pass

class MatchmakeView(GameBaseView, TemplateView):
    template_name = "game/matchmake.html"

    def get(self, request):
        if 'id' not in request.session: # chwilowe rozwiązanie
            request.session['id'] = random.randint(0, 1000000000)
        return super().get(request)

class MatchmakingQueueView(GameBaseView):
    @transaction.atomic
    def post(self, request):
        if MatchmakingQueueModel.is_in_queue(request.session['id']):
            record = MatchmakingQueueModel.objects.get(client_id=request.session['id'])
        else:
            record = MatchmakingQueueModel(client_id=request.session['id'])

        record.save()
        return HttpResponse(status=200)

class PairMakerView(GameBaseView):
    def post(self, request):
        if not MatchmakingQueueModel.is_in_queue(request.session['id']):
            raise Http404("Error in matchmaking algorithm")

        current_client = MatchmakingQueueModel.objects.get(client_id=request.session['id'])
        current_client.save()
        MatchmakingQueueModel.clean_queue()

        with transaction.atomic():
            current_client.delete()
            other_client = MatchmakingQueueModel.objects.order_by('time_added').first()

            if other_client is None:
                raise ObjectDoesNotExist()

            other_client.delete()
            game_session = GameSessionModel.create(current_client.client_id, other_client.client_id)
            game_session.save()

        return HttpResponseRedirect(reverse('game:game_session', args=[game_session.session_id]))

class GameSessionView(GameBaseView, TemplateView):
    template_name = "game/board.html"

    def get(self, request, session_id):
        if 'id' not in request.session: # chwilowe rozwiązanie
            return HttpResponseRedirect(reverse('game:matchmake'))

        game_session = GameSessionModel.objects.filter(session_id=session_id, status='ONGOING').first()

        if game_session is not None and (request.session['id'] in [game_session.white_player, game_session.black_player]):
            return super().get(request)

        return HttpResponseRedirect(reverse('game:matchmake'))        
import random
import datetime

from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from .models import MatchmakingQueueModel, GameSessionModel

class MatchmakeView(TemplateView):
    template_name = "game/matchmake.html"

    def get(self, request):
        if 'id' not in request.session: # chwilowe rozwiązanie
            request.session['id'] = random.randint(0, 1000000000)

        ongoing_session_id = GameSessionModel.get_ongoing_session_id(request.session['id'])

        if ongoing_session_id is not None:
            return HttpResponseRedirect(reverse('game:game_session', args=[ongoing_session_id]))
        
        return super().get(request)

class MatchmakingQueueView(View):
    @transaction.atomic
    def post(self, request):
        if MatchmakingQueueModel.is_in_queue(request.session['id']):
            record = MatchmakingQueueModel.objects.get(client_id=request.session['id'])
        else:
            record = MatchmakingQueueModel(client_id=request.session['id'])

        record.save()
        return HttpResponse(status=200)

class PairMakerView(View):
    def post(self, request):
        if (already_paired := GameSessionModel.get_ongoing_session_id(request.session['id'])) is not None:
            return HttpResponseRedirect(reverse('game:game_session', args=[already_paired]))
            
        if not MatchmakingQueueModel.is_in_queue(request.session['id']):
            raise Http404("Error in matchmaking algorithm")

        current_client = MatchmakingQueueModel.objects.get(client_id=request.session['id'])
        current_client.save()
        MatchmakingQueueModel.clean_queue()

        with transaction.atomic():
            current_client.delete()
            other_client = MatchmakingQueueModel.objects.order_by('pk').first()

            if other_client is None:
                raise ObjectDoesNotExist()

            other_client.delete()
            game_session = GameSessionModel.create(current_client.client_id, other_client.client_id)
            game_session.save()

        return HttpResponseRedirect(reverse('game:game_session', args=[game_session.session_id]))

class GameSessionView(TemplateView):
    template_name = "game/board.html"
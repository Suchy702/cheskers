import random
import datetime

from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from .models import WaitingListModel, GameSessionModel

class MatchmakeView(TemplateView):
    template_name = "game/matchmake.html"

    def get(self, request):
        if 'id' not in request.session:
            request.session['id'] = random.randint(0, 1000000000)

        ongoing_session_id = self.join_ongoing_session(request.session['id'])

        if ongoing_session_id is not None:
            return HttpResponseRedirect(reverse('game:game_session', args=[ongoing_session_id]))
        
        return super().get(request)

    def join_ongoing_session(self, player_id):
        as_white_player = GameSessionModel.objects.filter(white_player=player_id, status='ONGOING').first()
        if as_white_player is not None:
            return as_white_player.session_id

        as_black_player = GameSessionModel.objects.filter(black_player=player_id, status='ONGOING').first()
        if as_black_player is not None:
            return as_black_player.session_id

        return None

class WaitingList(View):
    def post(self, request):
        if self.is_already_in_queue(request.session['id']):
            record = WaitingListModel.objects.get(client_id=request.session['id'])
        else:
            record = WaitingListModel(client_id=request.session['id'])

        record.save()
        return HttpResponse(status=200)

    def is_already_in_queue(self, client_id):
        return len(WaitingListModel.objects.filter(client_id=client_id))

class PairMaker(View):
    @transaction.atomic
    def post(self, request):
        if (already_paired := self.already_paired(request.session['id'])) is not None:
            print(already_paired)
            return HttpResponseRedirect(reverse('game:game_session', args=[already_paired]))

        WaitingListModel.objects.get(client_id=request.session['id']).save()
        self.clean_waitinglist()

        current_client = WaitingListModel.objects.get(client_id=request.session['id'])
        current_client.delete()
        other_client = WaitingListModel.objects.order_by('pk').first()

        if other_client is None:
            raise ObjectDoesNotExist()

        other_client.delete()
        game_session = GameSessionModel.create(current_client.client_id, other_client.client_id)
        game_session.save()
        print(game_session)
        return HttpResponseRedirect(reverse('game:game_session', args=[game_session.session_id]))

    def clean_waitinglist(self):
        time_to_delete = datetime.datetime.now() - datetime.timedelta(seconds=90)
        WaitingListModel.objects.filter(time_added__lt=time_to_delete).delete()

    def already_paired(self, player_id):
        as_white_player = GameSessionModel.objects.filter(white_player=player_id, status='ONGOING').first()
        if as_white_player is not None:
            return as_white_player.session_id

        as_black_player = GameSessionModel.objects.filter(black_player=player_id, status='ONGOING').first()
        if as_black_player is not None:
            return as_black_player.session_id

        return None

class GameSessionView(TemplateView):
    template_name = "game/board.html"
import random

from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from .models import WaitingListModel, GameSessionModel

class MatchmakeView(TemplateView):
    template_name = "game/matchmake.html"

class WaitingList(View):
    def post(self, request):
        request.session['id'] = random.randint(0, 1000000000)
        record = WaitingListModel(client_id=request.session['id'])
        record.save()
        return HttpResponse(status=200)

class PairMaker(View):
    @transaction.atomic
    def post(self, request):
        current_client = WaitingListModel.objects.get(client_id=request.session['id'])
        current_client.delete()
        #WaitingListModel.objects.all().delete()
        other_client = WaitingListModel.objects.order_by('pk').first()

        if other_client is None:
            raise ObjectDoesNotExist()

        other_client.delete()
        game_session = GameSessionModel.create(current_client.client_id, other_client.client_id)
        print(game_session)
        return HttpResponseRedirect(reverse('game:game_session', args=[game_session.session_id]))

class GameSessionView(TemplateView):
    template_name = "game/board.html"
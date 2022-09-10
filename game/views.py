from django.contrib.auth.models import User
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
        client = PlayerModel.get_client_from_request(request)
        if MatchmakingQueueModel.is_in_queue(client):
            queue_entry = PlayerModel.objects_get_client(MatchmakingQueueModel.objects, client, 'client')
        else:
            queue_entry = MatchmakingQueueModel.create(client)

        queue_entry.save()
        return HttpResponse(status=200)


class PairMakerView(GameBaseView):
    def post(self, request):
        client = PlayerModel.get_client_from_request(request)
        if not MatchmakingQueueModel.is_in_queue(client):
            raise Http404("Error in matchmaking algorithm")

        current_client = PlayerModel.objects_get_client(MatchmakingQueueModel.objects, client, 'client')
        current_client.save()
        MatchmakingQueueModel.clean_queue()

        with transaction.atomic():
            current_client.delete()
            other_client = MatchmakingQueueModel.objects.order_by('last_updated').first()

            if other_client is None:
                raise ObjectDoesNotExist()

            other_client.delete()
            game_session = GameSessionModel.create(current_client.client, other_client.client)
            game_session.save()

        return HttpResponseRedirect(reverse('game:game_session', args=[game_session.session_url]))


class GameSessionView(GameBaseView, TemplateView):
    template_name = "game/board.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('show_invite', '') != '':
            link = self.request.META['PATH_INFO'].replace(reverse('game:game_session_prefix'), '')
            context['invite_message'] = f'Give your friend this link to play together: {link}'
        return context

    def get(self, request, session_id):
        game_session = GameSessionModel.updated_objects.filter(session_url=session_id).order_by('last_updated').first()

        if game_session is not None:
            client = PlayerModel.get_client_from_request(request)
            if self.is_authorized(client, game_session):
                if game_session.status == 'ONGOING':
                    return super().get(request)
                return HttpResponseRedirect(reverse('game:result', args=[session_id]))

        return HttpResponseRedirect(reverse('game:matchmake'))

    def is_authorized(self, client, game_session):
        if game_session.chess_player is not None and game_session.chess_player.get_client() == client:
            return True
        elif game_session.checkers_player is not None and game_session.checkers_player.get_client() == client:
            return True
        return False


class GuestLoginView(View):
    def get(self, request):
        PlayerModel.create_guest(request)
        return HttpResponseRedirect(reverse('game:matchmake'))


class ResultView(TemplateView):
    template_name = "game/result.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        game_session = GameSessionModel.updated_objects.filter(session_url=kwargs['session_url']).order_by('last_updated').first()
        client = PlayerModel.get_client_from_request(self.request)

        if game_session.status == 'ABORTED':
            context['result'] = 'ABORTED'
        else:
            me = 'CHESS' if client == game_session.chess_player.get_client() else 'CHECKERS'
            prefix = 'YOU' if game_session.status.startswith(me) else 'OPPONENT'
            suffix = game_session.status.split('_')[1]

            context['result'] = prefix + ' ' + suffix
        return context


class RankingView(TemplateView):
    template_name = "game/ranking.html"


class CreateRoomView(IDRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        player_client = PlayerModel.create(PlayerModel.get_client_from_request(request))
        player_client.save()
        game_session = GameSessionModel.create(None, player_client)
        game_session.save()
        return HttpResponseRedirect(reverse('game:game_session', args=[game_session.session_url])+"?show_invite=True")


class JoinRoomView(IDRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        game_session = GameSessionModel.get_ongoing_session_by_url(request.GET.get('room', ''))
        print(game_session)
        if game_session is None or game_session.chess_player is not None:
            return HttpResponseRedirect(reverse('game:matchmake'))

        player_client = PlayerModel.create(PlayerModel.get_client_from_request(request))
        player_client.save()
        game_session.chess_player = player_client
        game_session.save()
        return HttpResponseRedirect(reverse('game:game_session', args=[game_session.session_url]))


class PlayBotView(IDRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        player_client = PlayerModel.create(PlayerModel.get_client_from_request(request))
        player_client.save()
        game_session = GameSessionModel.create(player_client, None)
        game_session.against_bot = True
        game_session.save()
        return HttpResponseRedirect(reverse('game:game_session', args=[game_session.session_url]))
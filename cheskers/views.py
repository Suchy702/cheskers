import functools

from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect

from game.models import GameSessionModel, PlayerModel

class HomeView(TemplateView):
    template_name = "cheskers/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        if self.request.user.is_authenticated:
            client = PlayerModel.get_client_from_request(self.request)
            rows = []
            for row in PlayerModel.objects_filter_client(GameSessionModel.updated_objects, client, 'chess_player'):
                n_row = {}
                n_row['status'] = row.status
                n_row['time_finished'] = row.last_updated
                if row.against_bot:
                    n_row['opponent'] = 'Bot'
                else:
                    n_row['opponent'] = 'None' if row.checkers_player is None else 'Guest' if row.checkers_player.user is None else row.checkers_player.user.username
                n_row['which'] = 'chess'

                rows.append(n_row)

            for row in PlayerModel.objects_filter_client(GameSessionModel.updated_objects, client, 'checkers_player'):
                n_row = {}
                n_row['status'] = row.status
                n_row['time_finished'] = row.last_updated
                if row.against_bot:
                    n_row['opponent'] = 'Bot'
                else:
                    n_row['opponent'] = 'None' if row.chess_player is None else 'Guest' if row.chess_player.user is None else row.chess_player.user.username
                n_row['which'] = 'checkers'

                rows.append(n_row)

            rows.sort(key=functools.cmp_to_key(lambda a, b: b['time_finished'].timestamp() - a['time_finished'].timestamp()))
            context['rows'] = rows

        return context


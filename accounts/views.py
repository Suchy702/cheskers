import functools

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views import generic

from cheskers.mixins import LoginForbiddenMixin
from game.models import GameSessionModel, PlayerModel


class SignUpView(LoginForbiddenMixin, generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
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


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/update.html'
    fields = ['username', 'first_name', 'last_name', 'email']

    def get(self, request, pk, *args, **kwargs):
        if request.user.id != pk:
            return HttpResponseRedirect(reverse('profile'))
        return super().get(request, pk, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile')


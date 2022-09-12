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


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/update.html'
    fields = ['username', 'first_name', 'last_name', 'email']

    def get(self, request, pk, *args, **kwargs):
        if request.user.id != pk:
            return HttpResponseRedirect(reverse('home'))
        return super().get(request, pk, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')


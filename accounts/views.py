from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.views import generic

from cheskers.mixins import LoginForbiddenMixin

class SignUpView(LoginForbiddenMixin, generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile.html"
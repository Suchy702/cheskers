from django.shortcuts import render
from django.views.generic.base import TemplateView


class MatchmakeView(TemplateView):
    template_name = "game/matchmake.html"

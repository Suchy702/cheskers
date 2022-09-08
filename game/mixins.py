from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import PlayerModel

class IDRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if PlayerModel.get_client(request) is not None:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('home'))
from django.urls import reverse
from django.http import HttpResponseRedirect

class LoginForbiddenMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('home'))
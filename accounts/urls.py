from django.urls import path
from django.views.generic.base import TemplateView

from .views import SignUpView, ProfileView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('profile/', ProfileView.as_view(), name="profile")
]
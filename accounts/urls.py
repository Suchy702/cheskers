from django.urls import path
from django.views.generic.base import TemplateView

from .views import SignUpView, UpdateProfileView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('update/<int:pk>', UpdateProfileView.as_view(), name="update"),
]
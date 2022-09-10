from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    elo = models.IntegerField(default=1200)


def create_profile(sender, instance, created, **kwargs):
    if created:
        Info.objects.create(user=instance)


post_save.connect(create_profile, sender=User)

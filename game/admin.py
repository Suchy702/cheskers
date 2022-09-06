from django.contrib import admin

from .models import MatchmakingQueueModel, GameSessionModel 

admin.site.register(MatchmakingQueueModel)
admin.site.register(GameSessionModel)
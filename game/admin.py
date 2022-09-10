from django.contrib import admin

from .models import MatchmakingQueueModel, GameSessionModel, PlayerModel

admin.site.register(MatchmakingQueueModel)
admin.site.register(GameSessionModel)
admin.site.register(PlayerModel)
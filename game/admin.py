from django.contrib import admin

from .models import WaitingListModel, GameSessionModel 

admin.site.register(WaitingListModel)
admin.site.register(GameSessionModel)
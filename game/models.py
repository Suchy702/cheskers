import secrets
import datetime

from django.db import models

class WaitingListModel(models.Model):
    client_id = models.IntegerField()
    time_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.client_id)

class GameSessionModel(models.Model):
    white_player = models.IntegerField()
    black_player = models.IntegerField()
    session_id = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=(('ONGOING', 'ongoing'), ('FINISHED', 'finished'))
    )

    @classmethod
    def create(cls, white_player, black_player):
        session_id = secrets.token_urlsafe(16)
        game_session = cls(white_player=white_player, black_player=black_player, session_id=session_id, status='ONGOING')
        return game_session

    def __str__(self):
        return f'{self.white_player} {self.black_player} {self.session_id}, {self.status}'
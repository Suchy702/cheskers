import secrets
import datetime

from django.db import models

class MatchmakingQueueModel(models.Model):
    client_id = models.IntegerField()
    time_added = models.DateTimeField(auto_now=True)

    @staticmethod
    def is_in_queue(client_id):
        return len(MatchmakingQueueModel.objects.filter(client_id=client_id))

    @staticmethod
    def clean_queue():
        time_to_delete = datetime.datetime.now() - datetime.timedelta(seconds=10)
        MatchmakingQueueModel.objects.filter(time_added__lt=time_to_delete).delete()

    def __str__(self):
        return f'{self.client_id} {self.time_added}'

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

    @staticmethod
    def get_ongoing_session_id(player_id):
        as_white_player = GameSessionModel.objects.filter(white_player=player_id, status='ONGOING').first()
        if as_white_player is not None:
            return as_white_player.session_id

        as_black_player = GameSessionModel.objects.filter(black_player=player_id, status='ONGOING').first()
        if as_black_player is not None:
            return as_black_player.session_id

        return None

    def __str__(self):
        return f'{self.white_player} {self.black_player} {self.session_id}, {self.status}'
import secrets
import datetime

from django.db import models
from game.game_logic.logic_func import get_starting_board

class MatchmakingQueueModel(models.Model):
    client_id = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    @staticmethod
    def is_in_queue(client_id):
        return len(MatchmakingQueueModel.objects.filter(client_id=client_id))

    @staticmethod
    def clean_queue():
        time_to_delete = datetime.datetime.now() - datetime.timedelta(seconds=90)
        MatchmakingQueueModel.objects.filter(last_updated__lt=time_to_delete).delete()

    def __str__(self):
        return f'{self.client_id} {self.last_updated}'


class GameSessionModelManager(models.Manager):
    def get_queryset(self):
        time_to_delete = datetime.datetime.now() - datetime.timedelta(minutes=3)
        for obj in super().get_queryset().filter(last_updated__lt=time_to_delete):
            obj.status = 'ABORTED'
            obj.save()
        return super().get_queryset()

class GameSessionModel(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    white_player = models.IntegerField()
    black_player = models.IntegerField()
    session_id = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=(('ONGOING', 'ongoing'), ('FINISHED', 'finished'), ('ABORTED', 'aborted'))
    )
    which_player_turn = models.IntegerField()
    board = models.JSONField()

    objects = models.Manager()
    updated_objects = GameSessionModelManager()

    @classmethod
    def create(cls, white_player, black_player):
        session_id = secrets.token_urlsafe(16)
        game_session = cls(white_player=white_player, black_player=black_player, session_id=session_id,
                           status='ONGOING', which_player_turn=0, board=get_starting_board())
        return game_session

    @staticmethod
    def get_ongoing_session_by_id(player_id):
        as_white_player = GameSessionModel.updated_objects.filter(white_player=player_id, status='ONGOING').first()
        if as_white_player is not None:
            return as_white_player

        as_black_player = GameSessionModel.updated_objects.filter(black_player=player_id, status='ONGOING').first()
        if as_black_player is not None:
            return as_black_player

        return None

    @staticmethod
    def get_ongoing_session_by_url(url):
        return GameSessionModel.updated_objects.filter(session_id=url, status='ONGOING').first()

    @staticmethod
    def get_ongoing_session_id(player_id):
        session = GameSessionModel.get_ongoing_session_by_id(player_id)

        return None if session is None else session.session_id

    def __str__(self):
        return f'{self.white_player} {self.black_player} {self.session_id}, {self.status}'


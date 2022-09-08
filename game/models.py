import secrets
import datetime

from django.db import models
from django.contrib.auth.models import User
from game.game_logic.logic_func import get_starting_board


class PlayerModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    guest = models.IntegerField(null=True)

    @classmethod
    def create(cls, client):
        if client[1]:
            user_id = User.objects.get(pk=client[0])
            guest_id = None
        else:
            user_id = None
            guest_id = client[0]
        return cls(user=user_id, guest=guest_id)

    def get_id(self):
        if self.guest is not None:
            return self.guest, False
        return self.user.id, True

    @staticmethod
    def get_client(request):
        # True -> logged | False -> guest
        if request.user.is_authenticated:
            return request.user.id, True
        elif 'id' in request.session:
            return request.session['id'], False
        return None

    @staticmethod
    def create_guest(request):
        request.session['id'] = secrets.randbits(30)

    @staticmethod
    def objects_filter(objects, client):
        if client[1]:
            return objects.filter(client_id__user__pk=client[0])
        return objects.filter(client_id__guest=client[0])

    @staticmethod
    def objects_get(objects, client):
        if client[1]:
            return objects.get(client_id__user__pk=client[0])
        return objects.get(client_id__guest=client[0])


class MatchmakingQueueModel(models.Model):
    client_id = models.ForeignKey(PlayerModel, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, client):
        player = PlayerModel.create(client)
        player.save()
        return cls(client_id=player)

    @staticmethod
    def is_in_queue(client):
        return len(PlayerModel.objects_filter(MatchmakingQueueModel.objects, client))

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
    white_player = models.ForeignKey(PlayerModel, on_delete=models.CASCADE, related_name='+')
    black_player = models.ForeignKey(PlayerModel, on_delete=models.CASCADE, related_name='+')
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
    def create(cls, white_client, black_client):
        session_id = secrets.token_urlsafe(16)
        game_session = cls(white_player=white_client, black_player=black_client, session_id=session_id,
                           status='ONGOING', which_player_turn=0, board=get_starting_board())
        return game_session

    def get_remaining_time(self):
        return (self.last_updated + datetime.timedelta(minutes=3) - datetime.datetime.now(datetime.timezone.utc)).total_seconds()

    @staticmethod
    def get_ongoing_session_by_id(client):  # TODO refactor
        if client[1]:
            as_white_player = GameSessionModel.updated_objects.filter(white_player__user__pk=client[0],
                                                                      status='ONGOING').first()
            if as_white_player is not None:
                return as_white_player

            as_black_player = GameSessionModel.updated_objects.filter(black_player__user__pk=client[0],
                                                                      status='ONGOING').first()
            if as_black_player is not None:
                return as_black_player
        else:
            as_white_player = GameSessionModel.updated_objects.filter(white_player__guest=client[0],
                                                                      status='ONGOING').first()
            if as_white_player is not None:
                return as_white_player

            as_black_player = GameSessionModel.updated_objects.filter(black_player__guest=client[0],
                                                                      status='ONGOING').first()
            if as_black_player is not None:
                return as_black_player
        return None

    @staticmethod
    def get_ongoing_session_by_url(url):
        return GameSessionModel.updated_objects.filter(session_id=url, status='ONGOING').first()

    @staticmethod
    def get_ongoing_session_id(client):
        session = GameSessionModel.get_ongoing_session_by_id(client)

        return None if session is None else session.session_id

    def __str__(self):
        return f'{self.white_player} {self.black_player} {self.session_id}, {self.status}'

import secrets
import datetime
from typing import Optional

from django.db import models
from django.contrib.auth.models import User
from game.game_logic.logic_func import get_starting_board

# unique id, (true if logged in user, false if guest)
Client = tuple[int, bool]


class PlayerModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    guest = models.IntegerField(null=True)

    @classmethod
    def create(cls, client: Client):
        if client[1]:
            user_id = User.objects.get(pk=client[0])
            guest_id = None
        else:
            user_id = None
            guest_id = client[0]
        return cls(user=user_id, guest=guest_id)

    def get_client(self) -> Client:
        if self.guest is not None:
            return self.guest, False
        return self.user.id, True

    @staticmethod
    def get_client_from_request(request) -> Optional[Client]:
        if request.user.is_authenticated:
            return request.user.id, True
        elif 'id' in request.session:
            return request.session['id'], False
        return None

    @staticmethod
    def create_guest(request):
        request.session['id'] = secrets.randbits(30)

    @staticmethod
    def objects_filter_client(objects, client, attr_name, **kwargs):
        attr_name += '__user__pk' if client[1] else '__guest'
        attr = {attr_name: client[0]}

        return objects.filter(**attr, **kwargs)

    @staticmethod
    def objects_get_client(objects, client, attr_name, **kwargs):
        attr_name += '__user__pk' if client[1] else '__guest'
        attr = {attr_name: client[0]}

        return objects.get(**attr, **kwargs)


class MatchmakingQueueModel(models.Model):
    client = models.ForeignKey(PlayerModel, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, client: Client):
        player = PlayerModel.create(client)
        player.save()
        return cls(client=player)

    @staticmethod
    def is_in_queue(client: Client):
        return len(PlayerModel.objects_filter_client(MatchmakingQueueModel.objects, client, 'client'))

    @staticmethod
    def clean_queue():
        time_to_delete = datetime.datetime.now() - datetime.timedelta(seconds=90)
        MatchmakingQueueModel.objects.filter(last_updated__lt=time_to_delete).delete()

    def __str__(self):
        return f'{self.client} {self.last_updated}'


class GameSessionModelManager(models.Manager):
    def get_queryset(self):
        time_to_delete = datetime.datetime.now() - datetime.timedelta(minutes=3)
        for obj in super().get_queryset().filter(last_updated__lt=time_to_delete, status='ONGOING'):
            obj.handle_finished()
        return super().get_queryset()


class GameSessionModel(models.Model):
    chess_player = models.ForeignKey(PlayerModel, on_delete=models.CASCADE, related_name='+')
    checkers_player = models.ForeignKey(PlayerModel, on_delete=models.CASCADE, related_name='+')
    chess_player_joined = models.BooleanField(default=False)
    checkers_player_joined = models.BooleanField(default=False)
    session_url = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('ONGOING', 'ongoing'), ('ABORTED', 'aborted'), ('CHESS_WON', 'chess_won'),
            ('CHECKERS_WON', 'checkers_won'), ('CHESS_TIMEOUT', 'chess_timeout'),
            ('CHECKERS_TIMEOUT', 'checkers_timeout')
        )
    )
    which_player_turn = models.IntegerField(default=0)
    board = models.JSONField()

    objects = models.Manager()
    updated_objects = GameSessionModelManager()

    @classmethod
    def create(cls, chess_player, checkers_player):
        session_url = secrets.token_urlsafe(16)
        game_session = cls(chess_player=chess_player, checkers_player=checkers_player, session_url=session_url,
                           status='ONGOING', board=get_starting_board())
        return game_session

    def get_remaining_time(self):
        return (self.last_updated + datetime.timedelta(minutes=3) - datetime.datetime.now(datetime.timezone.utc)).total_seconds()

    def handle_finished(self):
        if self.status.endswith('WON'):
            return

        if not self.checkers_player_joined or not self.chess_player:
            self.status = 'ABORTED'
        elif self.which_player_turn == 0:
            self.status = 'CHESS_TIMEOUT'
        else:
            self.status = 'CHECKERS_TIMEOUT'

        self.save()

    @staticmethod
    def get_ongoing_session_by_client(client: Client):
        game_session = PlayerModel.objects_filter_client(GameSessionModel.updated_objects, client, 'chess_player', status='ONGOING').first()
        if game_session is not None:
            return game_session

        game_session = PlayerModel.objects_filter_client(GameSessionModel.updated_objects, client, 'checkers_player', status='ONGOING').first()
        if game_session is not None:
            return game_session

        return None

    @staticmethod
    def get_ongoing_session_by_url(url):
        return GameSessionModel.updated_objects.filter(session_url=url, status='ONGOING').first()

    @staticmethod
    def get_ongoing_session_url(client: Client):
        session = GameSessionModel.get_ongoing_session_by_client(client)

        return None if session is None else session.session_url

    def __str__(self):
        return f'{self.chess_player} {self.checkers_player} {self.session_url}, {self.status}'

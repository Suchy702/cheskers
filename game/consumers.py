import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import GameSessionModel
from game.game_logic.engine import Engine


class GameSessionConsumer(WebsocketConsumer):
    room_group_name = ''
    engine = Engine()

    def connect(self):
        self.accept()

    def initialize(self, data):
        self.room_group_name = data

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)

        self.send(text_data=json.dumps({
            'type': 'initialize',
            'remaining_time': session.get_remaining_time()
        }))

    def is_timeout(self):
        session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)
        return session is None

    def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json.get('message', '')
        message_type = data_json.get('type', '')

        if message_type == 'initialize':
            self.initialize(message)
        elif message_type == 'kill_session' or self.is_timeout():
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'kill_session',
                }
            )
        elif message_type == 'game_message':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'game_message',
                    'message': message
                }
            )

    def game_message(self, event):
        self.send(text_data=self.get_json_for_application(event['message']))

    def kill_session(self, event):
        session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)
        if session is not None:
            session.status = 'ABORTED'
            session.save()

        self.send(text_data=json.dumps({
            'type': 'kill_session'
        }))

    @staticmethod
    def _parse_command(command):
        from_, to = command.upper().split()
        return from_, to

    def get_json_for_application(self, command):
        from_, to = self._parse_command(command)

        curr_session = GameSessionModel.objects.get(session_id=self.room_group_name)
        board = curr_session.board

        is_move_legal = self.engine.check_move_legality(from_, to, board, curr_session.which_player_turn)
        if is_move_legal:
            self.engine.make_move(from_, to, board)
            curr_session.board = board
            curr_session.which_player_turn = (curr_session.which_player_turn+1) % 2
            curr_session.save()

        res = json.dumps({
            'board': board,
            'type': 'game_message',
            'remaining_time': curr_session.get_remaining_time(),
            'move_legality': is_move_legal
        })

        return res
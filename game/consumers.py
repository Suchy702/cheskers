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
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'game_message',
                    'message': message
                }
            )

    def game_message(self, event):
        from_, to = event['message'].split()
        curr_session = GameSessionModel.objects.get(session_id=self.room_group_name)
        board = curr_session.board

        is_move_legal = self.engine.check_move_legality(from_, to, board)
        if is_move_legal:
            self.engine.make_move(from_, to, board)
            curr_session.board = board
            curr_session.save()

        str_board_list = self.engine.get_str_board(board)

        self.send(text_data=json.dumps({
            'board_row_1': str_board_list[0],
            'board_row_2': str_board_list[1],
            'board_row_3': str_board_list[2],
            'board_row_4': str_board_list[3],
            'board_row_5': str_board_list[4],
            'board_row_6': str_board_list[5],
            'board_row_7': str_board_list[6],
            'board_row_8': str_board_list[7],
            'board_row_9': str_board_list[8],
            'board_row_10': str_board_list[9],
        }))

    def kill_session(self, event):
        session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)
        if session is not None:
            session.status = 'ABORTED'
            session.save()

        self.send(text_data=json.dumps({
            'type': 'kill_session'
        }))

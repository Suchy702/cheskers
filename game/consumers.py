import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import GameSessionModel, PlayerModel
from game.game_logic.engine import Engine


class GameSessionConsumer(WebsocketConsumer):
    room_group_name = ''
    engine = Engine()

    def connect(self):
        self.accept()

    def initialize(self, data):
        self.room_group_name = data
        self.who_am_i = self.get_who_am_i()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        game_session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)

        if self.who_am_i and not game_session.checkers_player_joined:
            game_session.checkers_player_joined = True
            game_session.save()
        elif not self.who_am_i and not game_session.chess_player_joined:
            game_session.chess_player_joined = True
            game_session.save()

        self.send(text_data=json.dumps({
            'type': 'initialize',
            'board': game_session.board,
            'remaining_time': game_session.get_remaining_time(),
            'all_legal_moves': self.engine.get_all_legal_moves(game_session.board),
            'which_player_turn': game_session.which_player_turn,
            'my_turn': self.is_my_turn(),
            'opponent': self.get_opponent()
        }))

    def is_timeout(self):
        return GameSessionModel.get_ongoing_session_by_url(self.room_group_name) is None

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
            self.handle_game_message(message)

    def handle_game_message(self, move):
        game_state = self.apply_move(move)
        if game_state is None:
            return
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': game_state
            }
        )

    def game_message(self, event):
        game_state = event['message']
        game_state['my_turn'] = self.is_my_turn()
        game_state['opponent'] = self.get_opponent()
        self.send(text_data=json.dumps(game_state))

    def kill_session(self, event):
        game_session = GameSessionModel.updated_objects.filter(session_url=self.room_group_name).order_by('-last_updated').first()
        game_session.handle_finished()

        self.send(text_data=json.dumps({
            'type': 'kill_session'
        }))

    @staticmethod
    def _parse_command(command):
        from_, to = command.upper().split()
        return from_, to

    def apply_move(self, command):
        from_, to = self._parse_command(command)

        game_session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)
        board = game_session.board

        is_move_legal = self.engine.check_move_legality(from_, to, board, game_session.which_player_turn)
        if is_move_legal:
            self.engine.make_move(from_, to, board)
            game_session.board = board
            game_session.which_player_turn = (game_session.which_player_turn+1) % 2
            game_session.save()

        if (won := self.engine.is_someone_won(board)) != 'NONE':
            game_session.status = 'CHESS_WON' if won == 'CHESS' else 'CHECKERS_WON'
            game_session.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'kill_session',
                }
            )
            return

        return {
            'board': board,
            'type': 'game_message',
            'remaining_time': game_session.get_remaining_time(),
            'move_legality': is_move_legal,
            'all_legal_moves': self.engine.get_all_legal_moves(board),
            'which_player_turn': game_session.which_player_turn,
        }

    def get_who_am_i(self):
        # 0 -> chess plater | 1 -> checkers player
        game_session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)

        if self.scope['user'].is_authenticated:
            player_client = self.scope['user'].id, True
        else:
            player_client = self.scope['session']['id'], False
        chess_client = game_session.chess_player.get_client()

        return 0 if player_client == chess_client else 1

    def get_opponent(self):
        game_session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)
        opponent = game_session.chess_player if self.who_am_i else game_session.checkers_player

        return opponent.user.username if opponent.user is not None else 'Guest'

    def is_my_turn(self):
        game_session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)
        return self.who_am_i == game_session.which_player_turn

from game.game_logic.jackstraws.jackstraw import Jackstraw
from game.game_logic.logic_func import is_in_chess_board, change_pos_name, is_checker_on_pos


class Pawn(Jackstraw):
    def __init__(self, pos: str = ''):
        super().__init__(pos, 'P')

    def _can_move_two_fields_forward(self, board: dict[str]) -> bool:
        return self.pos[1] == '2' and board[self.pos[0] + '3'] == board[self.pos[0] + '4'] == ''

    def _add_two_fields_forward_move(self, board: dict[str], moves: list[str]) -> None:
        if self._can_move_two_fields_forward(board):
            moves.append(self.pos[0] + '4')

    def _add_field_forward_move(self, board: dict[str], moves: list[str]) -> None:
        field_forward = change_pos_name(self.pos, 0, 1)
        if is_in_chess_board(field_forward) and board[field_forward] == '':
            moves.append(field_forward)

    def _add_beat_move(self, board: dict[str], moves: list[str], direction: int):
        beat = change_pos_name(self.pos, direction, 1)
        if is_in_chess_board(beat) and is_checker_on_pos(board[beat]):
            moves.append(beat)

    def get_legal_moves(self, board: dict[str]) -> list[str]:
        # zakladamy ze szachy zawsze sa biale
        moves = []
        self._add_two_fields_forward_move(board, moves)
        self._add_field_forward_move(board, moves)
        self._add_beat_move(board, moves, -1)
        self._add_beat_move(board, moves, 1)
        return moves


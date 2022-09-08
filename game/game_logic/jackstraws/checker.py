from .jackstraw import Jackstraw
from game.game_logic.logic_func import is_in_checker_board, change_pos_name, is_chess_on_pos


class Checker(Jackstraw):
    def __init__(self, pos: str = ''):
        super().__init__(pos, 'C')

    def _add_normal_moves(self, board: dict[str], moves: list[str]) -> None:
        directions = [(-1, -1), (1, -1)]
        for dirs in directions:
            new_pos = change_pos_name(self.pos, dirs[0], dirs[1])
            if is_in_checker_board(new_pos) and board[new_pos] == '.':
                moves.append(new_pos)

    def _add_beat_moves(self, board: dict[str], moves: list[str]) -> None:
        beat_dirs = [(-2, 0), (-2, 2), (0, 2), (2, 2), (2, 0), (2, -2), (0, -2), (-2, -2)]
        opon_dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        for b_dirs, o_dirs in zip(beat_dirs, opon_dirs):
            new_beat_pos = change_pos_name(self.pos, b_dirs[0], b_dirs[1])
            new_opon_pos = change_pos_name(self.pos, o_dirs[0], o_dirs[1])
            if is_in_checker_board(new_beat_pos) and board[new_beat_pos] == '.' and is_chess_on_pos(board[new_opon_pos]):
                moves.append(new_beat_pos)

    def get_legal_moves(self, board: dict[str]) -> list[str]:
        moves = []
        self._add_normal_moves(board, moves)
        self._add_beat_moves(board, moves)
        return moves


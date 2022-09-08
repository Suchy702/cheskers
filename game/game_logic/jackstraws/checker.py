from .jackstraw import Jackstraw
from game.game_logic.logic_func import is_in_checker_board, change_pos_name, is_chess_on_pos


class Checker(Jackstraw):
    def __init__(self, pos: str = ''):
        super().__init__(pos, 'C')
        self.moves = set()
        self.killed_opon = set()
        self.beat_dirs = [(-2, 0), (-2, 2), (0, 2), (2, 2), (2, 0), (2, -2), (0, -2), (-2, -2)]
        self.opon_dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    def _add_normal_moves(self, board: dict[str]) -> None:
        directions = [(-1, -1), (1, -1)]
        for dirs in directions:
            new_pos = change_pos_name(self.pos, dirs[0], dirs[1])
            if is_in_checker_board(new_pos) and board[new_pos] == '.':
                self.moves.add(new_pos)

    def _add_beat_moves(self, board: dict[str], pos: str) -> None:
        for b_dirs, o_dirs in zip(self.beat_dirs, self.opon_dirs):
            new_beat_pos = change_pos_name(pos, b_dirs[0], b_dirs[1])
            new_opon_pos = change_pos_name(pos, o_dirs[0], o_dirs[1])

            if not is_in_checker_board(new_beat_pos):
                continue
            
            if board[new_beat_pos] == '.' and is_chess_on_pos(board[new_opon_pos]) and new_beat_pos not in self.moves:
                self.moves.add(new_beat_pos)
                self.killed_opon.add(new_opon_pos)
                self._add_beat_moves(board, new_beat_pos)

    def get_legal_moves(self, board: dict[str]) -> list[str]:
        self.moves.clear()
        self._add_normal_moves(board)
        self._add_beat_moves(board, self.pos)
        return list(self.moves)

    def get_killed_oponents(self, board: dict[str, str]) -> list[str]:
        self.moves.clear()
        self.killed_opon.clear()
        self._add_beat_moves(board, self.pos)
        return list(self.killed_opon)

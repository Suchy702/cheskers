from .jackstraws.jackstraw import Jackstraw
from .jackstraws.pawn import Pawn
from .jackstraws.rook import Rook
from .jackstraws.queen import Queen
from .jackstraws.king import King
from .jackstraws.knight import Knight
from .jackstraws.bishop import Bishop
from .jackstraws.checker import Checker

from .logic_func import is_in_checker_board, is_pos_empty, is_chess_on_pos, is_checker_on_pos


class Engine:
    def __init__(self):
        self.jackstraws: dict[str, Jackstraw] = {
            'P': Pawn(),
            'R': Rook(),
            'Q': Queen(),
            'I': King(),
            'K': Knight(),
            'B': Bishop(),
            'C': Checker()
        }

    def _get_legal_moves(self, pos: str, board: dict[str, str]) -> list[str]:
        act_jackstraw = self.jackstraws[board[pos]]
        act_jackstraw.pos = pos
        return act_jackstraw.get_legal_moves(board)

    @staticmethod
    def _is_correct_player_move(which_player_move: int, obj: str) -> bool:
        if which_player_move == 0:
            return is_chess_on_pos(obj)
        else:
            return is_checker_on_pos(obj)

    def check_move_legality(self, from_: str, to: str, board: dict[str, str], which_player_move: int) -> bool:
        if not is_in_checker_board(from_):
            return False
        if is_pos_empty(board[from_]) or not self._is_correct_player_move(which_player_move, board[from_]):
            return False
        return to in self._get_legal_moves(from_, board)

    @staticmethod
    def _remove_chess_killed_by_checker(from_: str, to: str, board: dict[str, str]) -> None:
        pass

    def make_move(self, from_: str, to: str, board: dict[str, str]) -> None:
        if is_checker_on_pos(board[from_]):
            self._remove_chess_killed_by_checker(from_, to, board)
        board[to] = board[from_]
        board[from_] = '.'

    def is_someone_won(self, board: dict[str, str]) -> str:
        if board['A3'] == 'P':
            return 'CHESS'
        if board['D5'] == 'C':
            return 'CHECKER'
        return 'NONE'

    def get_all_legal_moves(self, board: dict[str, str]) -> dict[str, list[str]]:
        all_legal_moves = {}
        for key in board.keys():
            if not is_pos_empty(board[key]):
                all_legal_moves[key] = self._get_legal_moves(key, board)
        return all_legal_moves

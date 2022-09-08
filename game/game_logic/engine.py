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
        act_jackstraw = self.jackstraws[board[from_]]
        act_jackstraw.pos = from_
        legal_moves = act_jackstraw.get_legal_moves(board)
        return to in legal_moves

    @staticmethod
    def make_move(from_: str, to: str, board: dict[str, str]) -> None:
        board[to] = board[from_]
        board[from_] = '.'

    @staticmethod
    def get_str_board(board: dict[str, str]) -> list[str]:
        str_board = []
        lett = 'ZABCDEFGHI'
        nums = '9876543210'

        act = ''
        for i in range(len(nums)):
            for j in range(len(lett)):
                act += board[lett[j]+nums[i]].lower() + ' '
            str_board.append(act)
            act = ''
        return str_board

    def get_all_legal_moves(self, board: dict[str, str]) -> dict[str, list[str]]:
        all_legal_moves = {}
        for key in board.keys():
            if not is_pos_empty(board[key]):
                act_jackstraw = self.jackstraws[board[key]]
                act_jackstraw.pos = key
                all_legal_moves[key] = act_jackstraw.get_legal_moves(board)
        return all_legal_moves

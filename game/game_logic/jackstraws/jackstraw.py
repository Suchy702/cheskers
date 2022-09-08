from abc import ABC, abstractmethod
from game.game_logic.logic_func import change_pos_name, is_in_chess_board, is_checker_on_pos, is_pos_empty


class Jackstraw(ABC):
    def __init__(self, pos: str = '', name: str = ''):
        self.pos: str = pos
        self.name: str = name

    @abstractmethod
    def get_legal_moves(self, board: dict[str]) -> list[str]:
        pass

    def __str__(self):
        return self.name


class LineMovingJackstraw(Jackstraw, ABC):
    def get_moves_as_long_as_they_are_legal(self, board: dict[str], x_ch: int, y_ch: int) -> list[str]:
        act_pos = change_pos_name(self.pos, x_ch, y_ch)
        while is_in_chess_board(act_pos):
            if not is_pos_empty(board[act_pos]):
                if is_checker_on_pos(board[act_pos]):
                    yield act_pos
                break
            yield act_pos
            act_pos = change_pos_name(act_pos, x_ch, y_ch)

    def get_all_moves_in_given_dirs(self, board: dict[str], dirs: list[tuple[int, int]]) -> list[str]:
        moves = []
        for dir_ in dirs:
            moves.extend(self.get_moves_as_long_as_they_are_legal(board, dir_[0], dir_[1]))
        return moves


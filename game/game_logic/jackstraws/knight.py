from .jackstraw import Jackstraw
from game.game_logic.logic_func import is_in_chess_board, change_pos_name


class Knight(Jackstraw):
    def __init__(self, pos: str = ''):
        super().__init__(pos, 'knight')

    @property
    def poss_place_to_move(self) -> list[str]:
        y_change = [2, 2, -2, -2, 1, -1, 1, -1]
        x_change = [-1, 1, -1, 1, 2, 2, -2, -2]
        for y_ch, x_ch in zip(y_change, x_change):
            yield change_pos_name(self.pos, x_ch, y_ch)

    def get_legal_moves(self, board: dict[str]) -> list[str]:
        return [poss_move for poss_move in self.poss_place_to_move if is_in_chess_board(poss_move)]

from .jackstraw import Jackstraw
from game.game_logic.logic_func import get_all_moves_in_given_directions


class Knight(Jackstraw):
    def __init__(self, pos: str = ''):
        super().__init__(pos, 'rook')

    def get_legal_moves(self, board: dict[str]) -> list[str]:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return get_all_moves_in_given_directions(self.pos, board, directions)


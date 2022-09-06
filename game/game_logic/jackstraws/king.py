from .jackstraw import Jackstraw
from game.game_logic.logic_func import is_in_chess_board, change_pos_name


class King(Jackstraw):
    def __init__(self, pos: str = ''):
        super().__init__(pos, 'knight')

    def get_legal_moves(self, board: dict[str]) -> list[str]:
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dirs in directions:
            new_pos = change_pos_name(self.pos, dirs[0], dirs[1])
            if is_in_chess_board(new_pos):
                moves.append(new_pos)
        return moves

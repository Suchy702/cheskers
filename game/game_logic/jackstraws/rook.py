from .jackstraw import LineMovingJackstraw


class Rook(LineMovingJackstraw):
    def __init__(self, pos: str = ''):
        super().__init__(pos, 'rook')

    def get_legal_moves(self, board: dict[str]) -> list[str]:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return self.get_all_moves_in_given_dirs(board, directions)

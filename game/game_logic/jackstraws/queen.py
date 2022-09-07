from .jackstraw import LineMovingJackstraw


class Queen(LineMovingJackstraw):
    def __init__(self, pos: str = ''):
        super().__init__(pos, 'Q')

    def get_legal_moves(self, board: dict[str]) -> list[str]:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        return self.get_all_moves_in_given_dirs(board, directions)

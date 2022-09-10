from game.game_logic.engine import Engine
from random import choice


class GameBot:
    def __init__(self):
        self.engine = Engine()

    def get_decision(self, board: dict[str, str], play_as: str) -> tuple[str, str]:
        all_moves = self.engine.get_all_legal_moves(board)
        moves_to_decide = {}
        if play_as == 'checker':
            for key in all_moves:
                if board[key] == 'C' and len(all_moves[key]) > 0:
                    moves_to_decide[key] = all_moves[key]
        else:
            for key in all_moves:
                if board[key] != 'C' and len(all_moves[key]) > 0:
                    moves_to_decide[key] = all_moves[key]

        from_ = choice(list(moves_to_decide.keys()))
        to = choice(moves_to_decide[from_])
        return from_, to

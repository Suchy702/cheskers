from abc import ABC, abstractmethod


class Jackstraw(ABC):
    def __init__(self, pos: str = '', name: str = ''):
        self.pos: str = pos
        self.name: str = name

    @abstractmethod
    def get_legal_moves(self, board: dict[str]) -> list[str]:
        pass



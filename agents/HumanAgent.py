from sente import Game, Move, stone
from agents.ABCAgent import ABCAgent

class HumanAgent(ABCAgent):
    def __init__(self, game: Game, color: stone):
        super().__init__(game, color)

    def evaluate_board(self) -> float:
        return super().evaluate_board()

    def next_move(self):
        raw = input()
        x, y = raw.split()
        x = int(x)
        x -= 1
        y = int(y)
        y -= 1
        return Move(x, y, self.color)
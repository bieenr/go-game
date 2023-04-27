from sente import Game
import random
from agents.ABCAgent import ABCAgent

class RandomAgent(ABCAgent):
    def __init__(self, game: Game, color):
        super().__init__(game, color)

    def evaluate_board(self):
        return super().evaluate_board()

    def next_move(self):
        legal_moves = self.game.get_legal_moves()
        x = random.randint(0, len(legal_moves)-1)
        if legal_moves[x].get_x() == 19 or legal_moves[x].get_y() == 19:
            return None
        return legal_moves[x]
    
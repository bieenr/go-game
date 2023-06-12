from sente import Game
import random
from agents.ABCAgent import ABCAgent

class RandomAgent(ABCAgent):
    def __init__(self, game: Game, color):
        super().__init__(game, color)

    def evaluate_board(self):
        return self.game.score()[self.color] - self.game.score()[self.op_color]

    def next_move(self):
        if self.game.num_pass == 1 and self.evaluate_board() > 0:
            return None
        legal_moves = self.game.get_non_pss_moves()
        x = random.randint(0, len(legal_moves))
        if x == len(legal_moves):
            return None
        else:
            return legal_moves[x]

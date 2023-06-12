from sente import stone
from MyGame import MyGame as Game
from agents.ABCAgent import ABCAgent
from utils.constants import INF
import random

class AlphaBetaPruningAgent(ABCAgent):
    def __init__(self, game: Game, color: stone, depth: int):
        super().__init__(game, color)
        self.depth = depth
        self.n_opening_moves = 20
        self.seed = 0

    def get_shuffled_non_pss_moves(self):
        legal_moves = self.game.get_non_pss_moves()
        # random.seed(self.seed)
        # self.seed += 1
        random.shuffle(legal_moves)
        return legal_moves

    def evaluate_board(self):
        """
            A heuristic to evaluate the board's current state
        """
        return self.game.score()[self.color] - self.game.score()[self.op_color]

    def min_value(self, depth: int, alpha: float, beta: float):
        if depth == 0 or self.game.is_over():
            return None, self.evaluate_board()
        else:
            mov = None
            val = INF
            legal_moves = self.get_shuffled_non_pss_moves()
            for move in legal_moves:
                self.game.play(move)
                _, tmp_val = self.max_value(depth - 1, alpha, beta)
                if val > tmp_val:
                    val = tmp_val
                    mov = move
                if val <= alpha:
                    self.game.step_up()
                    return mov, val
                beta = min(beta, val)
                self.game.step_up()

            # try pass move
            if self.game.num_moves > self.n_opening_moves:
                self.game.pss()
                _, tmp_val = self.max_value(depth - 1, alpha, beta)
                if val > tmp_val:
                    val = tmp_val
                    mov = None
                if val <= alpha:
                    self.game.step_up()
                    return mov, val
                beta = min(beta, val)
                self.game.step_up()
            return mov, val

    def max_value(self, depth: int, alpha: float, beta: float):
        if depth == 0 or self.game.is_over():
            return None, self.evaluate_board()
        else:
            mov = None
            val = -INF
            legal_moves = self.get_shuffled_non_pss_moves()
            for move in legal_moves:
                self.game.play(move)
                _, tmp_val = self.min_value(depth - 1, alpha, beta)
                if val < tmp_val:
                    val = tmp_val
                    mov = move
                if val >= beta:
                    self.game.step_up()
                    return mov, val
                alpha = max(alpha, val)
                self.game.step_up()

            # try pass move
            if self.game.num_moves > self.n_opening_moves:
                self.game.pss()
                _, tmp_val = self.min_value(depth - 1, alpha, beta)
                if val < tmp_val:
                    val = tmp_val
                    mov = None
                if val >= beta:
                    self.game.step_up()
                    return mov, val
                alpha = max(alpha, val)
                self.game.step_up()
            return mov, val

    def find_move_alpha_beta(self, depth: int):
        move, _ = self.max_value(depth, -INF, INF)
        return move

    def next_move(self):
        sc = self.evaluate_board()
        if self.game.num_pass == 1 and sc > 0 and self.game.num_moves > self.n_opening_moves:
            return None
        if sc < -25 and self.game.num_moves > self.n_opening_moves:
            return None
        else:
            return self.find_move_alpha_beta(self.depth)

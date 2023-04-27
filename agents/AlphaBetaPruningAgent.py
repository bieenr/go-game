from sente import Game, stone
from agents.ABCAgent import ABCAgent
from utils.constants import INF

class AlphaBetaPruningAgent(ABCAgent):
    def __init__(self, game: Game, color: stone, depth: int):
        super().__init__(game, color)
        self.depth = depth

    def evaluate_board(self, opening_moves: int = 7):
        """
            A heuristic to evaluate the board's current state
        """
        num_pass = 0
        try:
            self.game.pss()
            num_pass += 1
            self.game.pss()
            num_pass += 1
        except:
            pass
        score = self.game.score()[self.color] - \
            self.game.score()[self.op_color]
        for _ in range(num_pass):
            self.game.step_up()
        return score

    def min_value(self, depth: int, alpha: float, beta: float):
        if depth == 0:
            return None, self.evaluate_board()
        else:
            mov = None
            val = INF
            legal_moves = self.game.get_legal_moves()
            for move in legal_moves:
                if move.get_x() == 19 or move.get_y() == 19:
                    # pass move
                    continue
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
            return mov, val

    def max_value(self, depth: int, alpha: float, beta: float):
        if depth == 0:
            return None, self.evaluate_board()
        else:
            mov = None
            val = -INF
            legal_moves = self.game.get_legal_moves()
            for move in legal_moves:
                if move.get_x() == 19 or move.get_y() == 19:
                    # pass move
                    continue

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
            return mov, val

    def find_move_alpha_beta(self, depth: int):
        move, _ = self.max_value(depth, -INF, INF)
        return move

    def next_move(self):
        return self.find_move_alpha_beta(self.depth)

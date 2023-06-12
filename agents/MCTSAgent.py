from sente import Move, stone, rules
from MyGame import MyGame as Game
from copy import deepcopy, copy
from agents.ABCAgent import ABCAgent
from math import sqrt, log
from tqdm import tqdm

class MCTSAgent(ABCAgent):
    def __init__(self, game: Game, color: stone, n_rollout: int, c: float):
        super().__init__(game, color)
        self.n_rollout = n_rollout
        self.c = c

    def evaluate_board(self) -> float:
        raise NotImplementedError

    def need_pss(self) -> bool:
        # pass when score < threshold
        raise NotImplementedError

    def rollout(self, move: Move) -> bool:
        copied_game = self.game
        print(copied_game)
        cnt = 0
        while not copied_game.is_over():
            print('rolling')
            move = copied_game.get_rand_non_pss_move()
            print(copied_game.get_non_pss_moves())
            print(move)
            copied_game.play(move)
            cnt += 1
            if cnt == 10:
                exit()
        return copied_game.get_winner() == self.colorp

    def uct_score(self, score) -> float:
        return score / self.n_rollout + self.c * \
            sqrt(log(self.n_rollout*len(self.game.get_non_pss_moves()))/self.n_rollout)

    def next_move(self) -> Move:
        chosen_move = None
        highest_score = -100000
        for move in self.game.get_non_pss_moves():
            score = 0
            for _ in tqdm(range(self.n_rollout)):
                score += self.rollout(move)
            if self.uct_score(score) > highest_score:
                highest_score = self.uct_score(score)
                chosen_move = move
        return chosen_move

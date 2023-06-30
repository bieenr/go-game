from sente import stone
from MyGame import MyGame as Game
from agents.ABCAgent import ABCAgent
from utils.constants import INF
import random
import numpy as np
from agents import AlphaBetaPruningAgent


class DropAgent(AlphaBetaPruningAgent):
    def __init__(self, game: Game, color: stone, depth: int, width: int=10):
        super().__init__(game, color, depth)
        self.width = width

    # def get_prop(self):
    #     if self.growing:
    #         if self.game.num_moves > 60:
    #             return 1.
    #         prop = self.base_prop * ((1. / self.base_prop) ** (1./60.)) ** self.game.num_moves
    #         return  prop
    #     else:
    #         return self.base_prop

    def get_candidate_moves(self):
        moves = super().get_candidate_moves()
        bfs_board = self.bfs_all()
        moves = sorted(moves, key=lambda move: bfs_board[move.get_x()][move.get_y()], reverse=True)
        candidates = [move for move in moves if bfs_board[move.get_x()][move.get_y()] > -10 and bfs_board[move.get_x()][move.get_y()] < 8.6]
        random.shuffle(candidates)
        if self.width < 1 and len(moves) > 0:
            return [moves[0]]
        elif self.width < 1 and len(moves) == 0:
            return []
        else:
            return candidates[:self.width]

    def bfs_all(self):
        b = self.game.get_board()
        result_board = np.zeros(b.shape)
        def bfs_one(i, j):
            q = [(i, j, 0)]
            visited = np.zeros(b.shape)
            ans = 0
            while len(q) > 0:
                (x, y, dist) = q.pop(0)
                if x < 0 or x >= b.shape[0] or y < 0 or y >= b.shape[1]:
                    continue
                if visited[x][y] == 1:
                    continue
                visited[x][y] = 1
                if b[x][y] == stone.EMPTY:
                    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                   (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        q.append((x + dx, y + dy, dist + 1))
                elif b[x][y] == self.color:
                    ans += 4 / dist**2
                else:
                    ans -= 4 / dist**2
            return ans
        
        for i in range(b.shape[0]):
            for j in range(b.shape[1]):
                if b[i][j] == stone.BLACK:
                    result_board[i][j] = INF
                elif b[i][j] == stone.WHITE:
                    result_board[i][j] = INF
                elif b[i][j] == stone.EMPTY:
                    result_board[i][j] = bfs_one(i, j)
        # return result_board
        random_board = np.random.choice(2, b.shape, p=[0.99, 0.01]) * np.random.normal(0, 9., b.shape)
        return result_board + random_board

if __name__ == "__main__":
    game = Game(9)
    agent = DropAgent(game, stone.BLACK, 3, 0.05, True)
    agent.bfs()

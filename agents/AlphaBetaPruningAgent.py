from sente import stone
from MyGame import MyGame as Game
from agents.ABCAgent import ABCAgent
from utils.constants import INF
import random
import numpy as np

class AlphaBetaPruningAgent(ABCAgent):
    def __init__(self, game: Game, color: stone, depth: int):
        super().__init__(game, color)
        self.depth = depth
        self.n_opening_moves = 20
        self.seed = 0

    def get_shuffled_non_pss_moves(self):
        legal_moves = self.game.get_non_pss_moves()
        random.shuffle(legal_moves)
        return legal_moves
    
    def evaluate_board(self, state):
        score = 0
        score += self.territory_score(state)  # Đánh giá lãnh thổ
        # print('***')
        # print(score)
        score -= self.attack_score(state)* 0.5  # Đánh giá tấn công
        # print(score)
        score += self.defense_score(state)* 0.3  # Đánh giá phòng thủ
        # print(score)
        score -= self.influence_score(state)* 0.2  # Đánh giá ảnh hưởng
        # print(score)
        score += self.blocking_score(state)* 0.4  # Đánh giá chặn đường đi của đối thủ
        score += self.Euler_number(state.get_board(),self.color)-self.Euler_number(state.get_board(),self.op_color) # Create an eye 
        # print(score)
        # print('***')
        return score

    def territory_score(self, state):
        # Tính toán điểm số lãnh thổ dựa trên độ chiếm đóng của mỗi người chơi
        # return self.game.score()[self.color] - self.game.score()[self.op_color]
        black_territory = self.count_territory(state.get_board(), self.color)
        white_territory = self.count_territory(state.get_board(), self.op_color)
        territory_score = black_territory - white_territory
        return territory_score

    def count_territory(self, board, player):
        # Đếm số lượng ô thuộc lãnh thổ của một người chơi
        territory = self.game.score()[player] - (self.game.get_board()==player).sum()
        # visited = set()

        # for i in range(9):
        #     for j in range(9):
        #         if (i, j) not in visited and board[i][j] == player:
        #             territory += self.explore_territory(board, player, i, j, visited)
        return territory

    def get_neighbors(self, board, x, y):
        neighbors = []
        n = 9
        if x > 0:
            neighbors.append((x - 1, y))
        if x < n - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < n - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def explore_territory(self, board, player, x, y, visited):
        queue = [(x, y)]
        territory = 0
        while queue:
            i, j = queue.pop(0)
            visited.add((i, j))
            territory += 1

            neighbors = self.get_neighbors(board, i, j)
            for neighbor in neighbors:
                ni, nj = neighbor
                if (ni, nj) not in visited and board[ni][nj] == player:
                    queue.append((ni, nj))
        return territory
    # def enough_9(self,board):
        

    def attack_score(self, state):
        # Đánh giá tấn công bằng cách đếm số lượng quân cờ tấn công đối thủ
        attack_score = self.count_stones(state.get_board(), self.op_color) 
        return attack_score

    def defense_score(self, state):
        # Đánh giá phòng thủ bằng cách đếm số lượng quân cờ phòng thủ của người chơi
        defense_score = self.count_stones(state.get_board(), self.color) 
        return defense_score

    def influence_score(self, state):
        # Đánh giá ảnh hưởng bằng cách đếm số lượng quân cờ gần biên giới của người chơi
        influence_score = self.count_boundary_stones(state.get_board(), self.color) 
        return influence_score

    def blocking_score(self, state):
        # Đánh giá chặn đường đi của đối thủ bằng cách đếm số lượng đường đi bị chặn
        blocking_score = self.count_blocked_paths(state.get_board(), self.op_color)
        return blocking_score

    def count_stones(self, board, player):
        # Đếm số lượng quân cờ của người chơi trên bàn cờ
        return np.sum(board == player)

    def count_boundary_stones(self, board, player):
        # Đếm số lượng quân cờ của người chơi gần biên giới
        count = 0
        n = 9
        for i in range(n):
            if board[i][0] == player:
                count += 1
            if board[i][n-1] == player:
                count += 1
            if board[0][i] == player:
                count += 1
            if board[n-1][i] == player:
                count += 1
        return count

    def count_blocked_paths(self, board, player):
        # Đếm số lượng đường đi bị chặn của đối thủ
        count = 0
        n = 9
        for i in range(n):
            for j in range(n):
                if board[i][j] == player:
                    neighbors = self.get_neighbors(board, i, j)
                    for neighbor in neighbors:
                        ni, nj = neighbor
                        if board[ni][nj] == stone.EMPTY:
                            count += 1
        return count
    def Euler_number(self, board, player):
        # heuristic count to create an eye
        Q1=0;
        Q3=0;
        Qd=0
        for i in range(8):
            for j in range(8):
                #Q1
                if board[i][j] == player and board[i+1][j] == stone.EMPTY and board[i][j+1] == stone.EMPTY and board[i+1][j+1] == stone.EMPTY:
                    Q1+=1
                if board[i][j] == stone.EMPTY and board[i+1][j] == player and board[i][j+1] == stone.EMPTY and board[i+1][j+1] == stone.EMPTY:
                    Q1+=1
                if board[i][j] == stone.EMPTY and board[i+1][j] == stone.EMPTY and board[i][j+1] == player and board[i+1][j+1] == stone.EMPTY:
                    Q1+=1
                if board[i][j] == stone.EMPTY and board[i+1][j] == stone.EMPTY and board[i][j+1] == stone.EMPTY and board[i+1][j+1] == player:
                    Q1+=1
                #Q3
                if board[i][j] == stone.EMPTY and board[i+1][j] == player and board[i][j+1] == player and board[i+1][j+1] == player:
                    Q3+=1
                if board[i][j] == player and board[i+1][j] == stone.EMPTY and board[i][j+1] == player and board[i+1][j+1] == player:
                    Q3+=1
                if board[i][j] == player and board[i+1][j] == player and board[i][j+1] == stone.EMPTY and board[i+1][j+1] == player:
                    Q3+=1
                if board[i][j] == player and board[i+1][j] == player and board[i][j+1] == player and board[i+1][j+1] == stone.EMPTY:
                    Q3+=1
                #Qd
                if board[i][j] == player and board[i+1][j] == stone.EMPTY and board[i][j+1] == stone.EMPTY and board[i+1][j+1] == player:
                    Qd+=1
                if board[i][j] == stone.EMPTY and board[i+1][j] == player and board[i][j+1] == player and board[i+1][j+1] == stone.EMPTY:
                    Qd+=1
        return (10/self.game.num_moves*(Q1-Q3)-abs(35-self.game.num_moves)*2*Qd)/4

    def min_value(self, depth: int, alpha: float, beta: float):
        if depth == 0 or self.game.is_over():
            return None, self.evaluate_board(self.game)
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
            return None, self.evaluate_board(self.game)
        else:
            mov = None
            val = -INF
            init_sc = self.game.score()[self.color] - self.game.score()[self.op_color]
            new_sc = -INF
            if self.game.num_moves > self.n_opening_moves:
                self.game.pss()
                op_move, tmp_val = self.min_value(depth - 1, alpha, beta)
                self.game.play(op_move)
                new_sc = self.game.score()[self.color] - self.game.score()[self.op_color]
                self.game.step_up()
                self.game.step_up()
            
            if self.game.num_moves>=60:
                if new_sc - init_sc >= 0:
                    return None, self.evaluate_board(self.game)
            else: 
                if new_sc - init_sc > 0:
                    return None, self.evaluate_board(self.game)
                
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
            # if self.game.num_moves > self.n_opening_moves:
            #     self.game.pss()
            #     _, tmp_val = self.min_value(depth - 1, alpha, beta)
            #     if val < tmp_val:
            #         val = tmp_val
            #         mov = None
            #     if val >= beta:
            #         self.game.step_up()
            #         return mov, val
            #     alpha = max(alpha, val)
            #     self.game.step_up()
            return mov, val

    def find_move_alpha_beta(self, depth: int):
        move, val = self.max_value(depth, -INF, INF)
        print(val)
        return move

    def next_move(self):
        sc = self.game.score()[self.color] - self.game.score()[self.op_color]
        if self.game.num_pass == 1 and sc > 0 and self.game.num_moves > self.n_opening_moves:
            return None
        if sc < -15 and self.game.num_moves > self.n_opening_moves:
            return None
        else:
            return self.find_move_alpha_beta(self.depth)

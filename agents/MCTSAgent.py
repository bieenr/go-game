from sente import Move, stone
from MyGame import MyGame as Game
from agents.ABCAgent import ABCAgent
import random
from collections import defaultdict
import math


class MCTS:
    def __init__(self, exploration_weight=1):
        self.sum_reward = defaultdict(int)
        self.n_visit = defaultdict(int)
        self.children = dict()
        self.exploration_weight = exploration_weight

    def choose(self, node):
        "Choose the best child"
        if node.is_terminal():
            raise RuntimeError(f"Can't choose from a terminal node: {node}")
        if node not in self.children:
            return node.get_random_child()
        
        def score(n):
            if self.n_visit[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.sum_reward[n] / self.n_visit[n]  # average reward

        return max(self.children[node], key=score)

    def rollout(self, node):
        "~train"
        path_to_new_node = self.select(node)
        new_node = path_to_new_node[-1]
        self.expand(new_node)
        reward = self.simulate(new_node)
        self.backprop(path_to_new_node, reward)

    def select(self, node):
        "Find an unexplored descendent"
        path_to_new_node = []
        while True:
            path_to_new_node.append(node)
            if node not in self.children or not self.children[node]:
                # unexplored or terminal node
                return path_to_new_node
            new_node = self.children[node] - self.children.keys()
            if new_node:
                n = new_node.pop()
                path_to_new_node.append(n)
                return path_to_new_node
            node = self.UCT(node)  # descend a layer deeper

    def expand(self, node):
        "Update the children dict"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.get_all_children()

    def simulate(self, node):
        "random simulation"
        my_turn = True
        while True:
            if node.is_terminal():
                reward = node.reward()
                return 1 - reward if my_turn else reward
            node = node.get_random_child()
            my_turn = not my_turn

    def backprop(self, path, reward):
        "Update node values from leaf to root"
        for node in reversed(path):
            self.n_visit[node] += 1
            self.sum_reward[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def UCT(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.n_visit[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.sum_reward[n] / self.n_visit[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.n_visit[n]
            )

        return max(self.children[node], key=uct)


class GoState:
    def __init__(self, seq, color):
        self.color = color
        if self.color == stone.BLACK:
            self.op_color = stone.WHITE
        else:
            self.op_color = stone.BLACK
        self.seq = seq
        self.game = Game()
        self.game.play_sequence(seq)

    def get_all_children(self):
        lm = self.game.get_legal_moves()
        if len(lm) == 0:
            return set()
        else:
            return set([GoState(self.seq + [m], self.color) for m in lm])
    
    def get_random_child(self):
        lm = self.game.get_legal_moves()
        if len(lm) == 0:
            return None
        rand_ind = random.randint(0, len(lm) - 1)
        return GoState(self.seq + [lm[rand_ind]], self.color)
    
    def is_terminal(self):
        if self.game.num_moves > 10 and \
            (self.game.score()[stone.BLACK] - self.game.score()[stone.WHITE] >= 20 \
            or self.game.score()[stone.WHITE] - self.game.score()[stone.BLACK] >= 20):
            return True
        return self.game.is_over()
    
    def reward(self):
        return self.game.score()[self.color] - self.game.score()[self.op_color]


class MCTSAgent(ABCAgent):
    def __init__(self, game, color):
        super().__init__(game, color)
        self.tree = MCTS()

    def next_move(self) -> Move:
        cur_node = GoState(self.game.get_current_sequence(), self.color)
        for _ in range(50):
            self.tree.rollout(cur_node)
        new_node = self.tree.choose(cur_node)
        return new_node.seq[-1]
    
    def evaluate_board(self) -> float:
        return 0
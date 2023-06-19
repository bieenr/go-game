"""
    This is a Game class inherited from sente.Game.
    Can use as a drop-in replacement for sente.Game.
    The difference is that when step up from a game state, the result of
        is_over() will be reset to False.
"""
from sente import Game, rules, Move
from MyStack import MyStack
from random import randint
from copy import deepcopy

class MyGame(Game):
    def __init__(self, size=9, rules=rules.CHINESE):
        super().__init__(size, rules)
        self.num_pass = 0
        self.num_moves = 0
        self.num_pass_stack = MyStack(maxsize=20)
        self.num_pass_stack.put(0)

    def __str__(self):
        arr = super().numpy()
        s = ""
        for i in range(9):
            for j in range(9):
                if arr[i][j][0] == 1:
                    s += 'b'
                elif arr[i][j][1] == 1:
                    s += 'W'
                else:
                    s += '.'
            s += '\n'
        return s[:-1]

    def score(self):
        n_pss = 0
        try:
            self.pss()
            n_pss += 1
            self.pss()
            n_pss += 1
        except:
            pass
        score = super().score()
        for _ in range(n_pss):
            self.step_up()
        return score

    def play(self, *args):
        if isinstance(args[0], Move):
            move = args[0]
            self.num_pass = 0
            self.num_moves += 1
            self.num_pass_stack.put(0)
            if self.is_over():
                raise Exception("Game is over")

            super().play(move)
        
        else:
            self.num_pass = 0
            self.num_moves += 1
            self.num_pass_stack.put(0)
            super().play(args[0], args[1])

    def pss(self):
        super().pss()
        self.num_moves += 1
        self.num_pass += 1
        self.num_pass_stack.put(self.num_pass)

    def step_up(self):
        super().step_up()
        self.num_pass = self.num_pass_stack.pop()
        self.num_pass = self.num_pass_stack.top()
        self.num_moves -= 1

    def is_over(self):
        return self.num_pass_stack.top() >= 2
    
    def get_legal_moves(self):
        if self.is_over():
            return []
        else:
            return super().get_legal_moves()
    
    def get_non_pss_moves(self):
        moves = self.get_legal_moves()
        return [move for move in moves if move.get_x() != 19 and move.get_y() != 19]
    
    def get_rand_non_pss_move(self):
        moves = self.get_non_pss_moves()
        return moves[randint(0, len(moves) - 1)]
    
    def get_rand_move(self):
        moves = self.get_legal_moves()
        return moves[randint(0, len(moves) - 1)]

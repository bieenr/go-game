"""
    This is a Game class inherited from sente.Game.
    Can use as a drop-in replacement for sente.Game.
    The difference is that when step up from a game state, the result of
        is_over() will be reset to False.
"""
from sente import Game, rules, Move, stone
from MyStack import MyStack
from random import randint
from copy import deepcopy
import numpy as np
import time


class MyGame(Game):
    def __init__(self, size=9, rules=rules.CHINESE, time_limit=None):
        super().__init__(size, rules)
        self.num_pass = 0
        self.num_moves = 0
        self.num_pass_stack = MyStack(maxsize=20)
        self.num_pass_stack.put(0)
        # self.start_time = time.time()
        self.cur_move_start_time = time.time()
        self.time_used = {stone.BLACK: 0, stone.WHITE: 0}
        self.time_limit = 0 if time_limit is None else time_limit * 60

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

    def get_board(self):
        boardnp = (np.argmax(self.numpy(), axis=2)+1) % 3
        return boardnp

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
            if move.get_x() != 19:
                self.num_pass = 0
                self.num_moves += 1
                self.num_pass_stack.put(0)
                if self.is_over():
                    raise Exception("Game is over")
                super().play(move)
            else:
                self.pss()
        elif args[0] is None:
            self.pss()
        else:
            self.num_pass = 0
            self.num_moves += 1
            self.num_pass_stack.put(0)
            super().play(args[0], args[1])

    def play_time(self, *args):
        if isinstance(args[0], Move):
            move = args[0]
            if move.get_x() != 19:
                self.num_pass = 0
                self.num_moves += 1
                self.num_pass_stack.put(0)
                if self.is_over():
                    raise Exception("Game is over")
                super().play(move)
            else:
                self.pss()
        elif args[0] is None:
            self.pss()
        else:
            self.num_pass = 0
            self.num_moves += 1
            self.num_pass_stack.put(0)
            super().play(args[0], args[1])
        cur_player = self.get_active_player()
        op_player = stone.WHITE if cur_player == stone.BLACK else stone.BLACK
        self.time_used[op_player] = self.time_used[op_player] + \
            time.time() - self.cur_move_start_time
        self.cur_move_start_time = time.time()

    def play_sequence(self, seq):
        for move in seq:
            self.play(move)

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
        # if (self.time_limit != 0):
        #     if (self.get_remain_time(player=self.get_active_player()) <= 0):
        #         return True
        return self.num_pass_stack.top() >= 2

    def get_legal_moves(self):
        if self.is_over():
            return []
        else:
            return super().get_legal_moves()[:-1]

    def get_non_pss_moves(self):
        moves = self.get_legal_moves()
        return [move for move in moves if move.get_x() != 19 and move.get_y() != 19]

    def get_rand_non_pss_move(self):
        moves = self.get_non_pss_moves()
        return moves[randint(0, len(moves) - 1)]

    def get_rand_move(self):
        moves = self.get_legal_moves()
        return moves[randint(0, len(moves) - 1)]

    def get_used_time(self, player=stone.BLACK):
        if self.get_active_player() == player:
            return self.time_used[player] + time.time() - self.not_active_player
        else:
            return self.time_used[player]

    def get_remain_time(self, player=stone.BLACK):
        if (self.time_limit != 0):
            return self.time_limit - self.get_used_time(player)
        else:
            return 0

    def convert_time(self, second):
        return str(int(second//60)) + ":" + str(int(second % 60))

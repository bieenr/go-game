from sente import stone
from MyGame import MyGame as Game
from agents.ABCAgent import ABCAgent
from utils.constants import INF
import random
import numpy as np
import re
import time
from agents import AlphaBetaPruningAgent


class GreedyAgent(AlphaBetaPruningAgent):
    def __init__(self, game: Game, color: stone):
        super().__init__(game, color, depth=1)

    def evaluate_board(self, state):
        return self.game.score()[self.color] - self.game.score()[self.op_color]
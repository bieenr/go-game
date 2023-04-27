from sente import Game, stone, Move, rules
import time
from tqdm import tqdm
import random
from agents import AlphaBetaPruningAgent, HumanAgent, RandomAgent


if __name__ == "__main__":
    game = Game(9, rules=rules.CHINESE)
    agentBlack = AlphaBetaPruningAgent(game, stone.BLACK, 3)
    agentWhite = RandomAgent(game, stone.WHITE)
    num_pass = 0
    while True:
        move = agentBlack.next_move()
        if move is None:
            game.pss()
            print('black pass')
            num_pass += 1
        else:
            num_pass = 0
            print(move)
            game.play(move)
        print(game)
        print(game.score()['result'])
        if num_pass == 2:
            print("Game over")
            print(f'the winner is {game.get_winner()} with {game.score()}')
        move = agentWhite.next_move()
        if move is None:
            game.pss()
            print('white pass')
            num_pass += 1
        else:
            num_pass = 0
            print(move)
            game.play(move)
        print(game)
        print(game.score()['result'])
        if num_pass == 2:
            print("Game over")
            print(f'the winner is {game.get_winner()} with {game.score()}')

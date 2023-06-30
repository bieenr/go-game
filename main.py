from sente import stone, Move, rules
from MyGame import MyGame as Game
import time
import datetime
from tqdm import tqdm
import random
from agents import AlphaBetaPruningAgent, HumanAgent, RandomAgent, MCTSAgent, DropAgent
import logging
import argparse
import os


if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--black', type=str, default='ab', help='black '
                        + 'agent, choose from ab (alpha-beta), rand (random),'
                        + ' mcts (monte-carlo tree search))')
    parser.add_argument('--white', type=str, default='ab', help='white '
                        + 'agent, choose from ab (alpha-beta), rand (random),'
                        + ' mcts (monte-carlo tree search)')
    parser.add_argument('--bdepth', type=int, default=3, help='depth of '
                        + 'alpha-beta pruning for black')
    parser.add_argument('--wdepth', type=int, default=3, help='depth of '
                        + 'alpha-beta pruning for white')
    parser.add_argument('--n_opening_moves', type=int, default=20, help='number '
                        + 'of opening moves')
    parser.add_argument('--brollout', type=int, default=100, help='number of '
                        + 'rollouts for black')
    parser.add_argument('--wrollout', type=int, default=100, help='number of '
                        + 'rollouts for white')
    parser.add_argument('--bwidth', type=int, default=10, help='number of children expand for black')
    parser.add_argument('--wwidth', type=int, default=10, help='number of children expand for white')
    args = parser.parse_args()


    # logger
    formatter = logging.Formatter('%(message)s')
    gameLogger = logging.getLogger("gameLogger")
    gameLogger.setLevel(logging.INFO)
    dt = datetime.datetime.now()
    game_log_foldername = 'log/' + args.black \
                        + '_' + (str(args.bdepth) if args.black == 'ab' or args.black=='drop' else '') \
                        + ('_' + str(args.bwidth) if args.black == 'drop' else '') \
                        + '_' + args.white \
                        + '_' + (str(args.wdepth) if args.white == 'ab' or args.white=='drop' else '') \
                        + ('_' + str(args.wwidth) if args.white == 'drop' else '')
    if not os.path.exists(game_log_foldername):
        os.makedirs(game_log_foldername)
    game_log_file_name =  str(datetime.datetime.timestamp(dt)) + '.log'
    game_log_file_handler = logging.FileHandler(game_log_foldername + '/' + game_log_file_name)
    game_log_file_handler.setFormatter((formatter))
    gameLogger.addHandler(game_log_file_handler)


    # game
    game = Game(9, rules=rules.CHINESE, time_limit=1)
    if args.black == 'ab':
        agentBlack = AlphaBetaPruningAgent(game, stone.BLACK, args.bdepth)
    elif args.black == 'rand':
        agentBlack = RandomAgent(game, stone.BLACK)
    elif args.black == 'mcts':
        agentBlack = MCTSAgent(game, stone.BLACK)
    elif args.black == 'drop':
        agentBlack = DropAgent(game, stone.BLACK, args.bdepth, args.bwidth)
    else:
        raise Exception('Invalid black agent')
    
    if args.white == 'ab':
        agentWhite = AlphaBetaPruningAgent(game, stone.WHITE, args.wdepth)
    elif args.white == 'rand':
        agentWhite = RandomAgent(game, stone.WHITE)
    elif args.white == 'mcts':
        agentWhite = MCTSAgent(game, stone.WHITE)
    elif args.white == 'drop':
        agentWhite = DropAgent(game, stone.WHITE, args.wdepth, args.wwidth)
    else:
        raise Exception('Invalid white agent')

    turn = 0
    while game.is_over() is False:
        begin_time = time.time()
        if turn == 0:
            move = agentBlack.next_move()
        else:
            move = agentWhite.next_move()
        gameLogger.info(move)
        if move is None:
            game.pss()
            gameLogger.info('black pass' if turn==0 else 'white pass')
        else:
            game.play_time(move)
        turn = 1 - turn
        gameLogger.info(game.__str__())
        gameLogger.info(f'game num_moves: {game.num_moves}')
        gameLogger.info(f'game num_pass: {game.num_pass}')
        gameLogger.info(f'game score: {game.score()["result"]}')
        gameLogger.info(f'time usedd: {time.time() - begin_time}')
        gameLogger.info('\n')
    if game.score()['result'][0] == 'B':
        gameLogger.info('Black wins')
    else:
        gameLogger.info('White wins')

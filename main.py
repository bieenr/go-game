from sente import stone, Move, rules
from MyGame import MyGame as Game
import time
import datetime
from agents import AlphaBetaPruningAgent, RandomAgent, MCTSAgent, DropAgent, GreedyAgent
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
    parser.add_argument('--bdepth', type=int, default=2, help='depth of '
                        + 'alpha-beta pruning for black')
    parser.add_argument('--wdepth', type=int, default=2, help='depth of '
                        + 'alpha-beta pruning for white')
    parser.add_argument('--n_opening_moves', type=int, default=20, help='number '
                        + 'of opening moves')
    parser.add_argument('--brollout', type=int, default=100, help='number of '
                        + 'rollouts for black')
    parser.add_argument('--wrollout', type=int, default=100, help='number of '
                        + 'rollouts for white')
    parser.add_argument('--bwidth', type=int, default=10, help='number of children expand for black')
    parser.add_argument('--wwidth', type=int, default=10, help='number of children expand for white')
    parser.add_argument('--time-limit', type=int, default=-1, help='number of time (minutes) for each side, set <0 if play unlimited time')
    args = parser.parse_args()


    # logger
    formatter = logging.Formatter('%(message)s')
    gameLogger = logging.getLogger("gameLogger")
    gameLogger.setLevel(logging.INFO)
    dt = datetime.datetime.now()
    game_log_foldername = 'log/' + args.black \
                        + '_' + (str(args.bdepth) if args.black in ['ab', 'drop', 'greedy'] else '') \
                        + ('_' + str(args.bwidth) if args.black == 'drop' else '') \
                        + '_' + args.white \
                        + '_' + (str(args.wdepth) if args.white in ['ab', 'drop', 'greedy'] else '') \
                        + ('_' + str(args.wwidth) if args.white == 'drop' else '') \
                        + ('_time' + str(args.time_limit) if args.time_limit > 0 else '')
    if not os.path.exists(game_log_foldername):
        os.makedirs(game_log_foldername)
    game_log_file_name =  str(datetime.datetime.timestamp(dt)) + '.log'
    game_log_file_handler = logging.FileHandler(game_log_foldername + '/' + game_log_file_name)
    game_log_file_handler.setFormatter((formatter))
    gameLogger.addHandler(game_log_file_handler)


    # game
    if args.time_limit < 0:
        TL = None
    else:
        TL = args.time_limit
    game = Game(9, rules=rules.CHINESE, time_limit=TL)
    if args.black == 'ab':
        agentBlack = AlphaBetaPruningAgent(game, stone.BLACK, args.bdepth)
    elif args.black == 'rand':
        agentBlack = RandomAgent(game, stone.BLACK)
    elif args.black == 'mcts':
        agentBlack = MCTSAgent(game, stone.BLACK)
    elif args.black == 'drop':
        agentBlack = DropAgent(game, stone.BLACK, args.bdepth, args.bwidth)
    elif args.black == 'greedy':
        agentBlack = GreedyAgent(game, stone.BLACK, args.bdepth)
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
    elif args.white == 'greedy':
        agentWhite = GreedyAgent(game, stone.WHITE, args.wdepth)
    else:
        raise Exception('Invalid white agent')

    turn = 0
    time_mode = True if args.time_limit > 0 else False
    while game.is_over() is False:
        begin_time = time.time()
        if turn == 0:
            move = agentBlack.next_move(time_mode)
        else:
            move = agentWhite.next_move(time_mode)
        gameLogger.info(move)
        if move is None:
            game.pss()
            gameLogger.info('black pass' if turn==0 else 'white pass')
        else:
            game.play_time(move)
        gameLogger.info(game.__str__())
        gameLogger.info(f'game num_moves: {game.num_moves}')
        gameLogger.info(f'game num_pass: {game.num_pass}')
        gameLogger.info(f'game score: {game.score()["result"]}')
        gameLogger.info(f'time used: {time.time() - begin_time}')
        gameLogger.info(f'remaining time: {game.get_remain_time(stone.BLACK) if turn==0 else game.get_remain_time(stone.WHITE)}')
        gameLogger.info('\n')
        turn = 1 - turn
    if game.score()['result'][0] == 'B':
        gameLogger.info('Black wins')
    else:
        gameLogger.info('White wins')

import abc
from sente import Game, Move, stone

class ABCAgent(abc.ABC):
    def __init__(self, game: Game, color: stone):
        self.game = game
        self.color = color
        if self.color == stone.BLACK:
            self.op_color = stone.WHITE
        else:
            self.op_color = stone.BLACK

    @abc.abstractmethod
    def evaluate_board(self) -> float:
        """
            A heuristic to evaluate the board's current state
        """
        return 0
    
    @abc.abstractmethod
    def next_move(self) -> Move:
        """
            Returns the next move to be played by the agent
        """
        return None
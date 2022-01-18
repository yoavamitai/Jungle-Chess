from math import inf 
import time
from typing import TYPE_CHECKING

COORDINATES = tuple[int, int]
RANK_DEVELOPMENT = {
    1: [[8,8,8,0,8,8,8], 
        [8,8,8,9,9,9,9],
        [8,8,8,9,10,10,10],
        [8,9,9,10,12,12,11],
        [8,9,9,11,12,12,12],
        [8,9,9,11,12,12,13],
        [10,11,11,13,13,13,13],
        [11,12,13,50,13,13,13],
        [11,13,50, 9999, 50, 13, 13]],
    
}
class Move:
    def __init__(self, start: COORDINATES, target: COORDINATES):
        """Represents a general move which can be performed and reverted on different boards

        Args:
            start (COORDINATES): starting piece index
            target (COORDINATES): target piece index
        """
        self.start = start
        self.target = target
        self.is_capturing = False
        self.captured = None
    
    def __iter__(self) -> iter:
        return iter(self.start + self.target)
    
    def perform(self, board) -> None:
        """Perform a move on a given board.

        Args:
            board (List[int, int]): given game board
        """
        # Capture piece
        if board[self.target[0], self.target[1]] != 0:
            self.is_capturing = True
            self.captured = board[self.target[0], self.target[1]]
            board[self.target[0], self.target[1]] = 0
        
        # Move piece
        tmp = board[self.start[0], self.start[1]]
        board[self.start[0], self.start[1]] = 0
        board[self.target[0], self.target[1]] = tmp
    
    def revert(self, board) -> None:
        """Revert a move done on a given board.

        Args:
            board (list[int, int]): given game board
        """
        
        # Revert capture
        if self.is_capturing:
            board[self.target[0], self.target[1]] = self.captured
        
        # Revert piece Movement
        tmp = board[self.start[0], self.start[1]]
        board[self.start[0], self.start[1]] = board[self.target[0], self.target[1]]
        board[self.target[0], self.target[1]] = tmp
          
def is_win(board, player: str) -> bool:
    """check if given player won the game

    Args:
        board (list[int, int]): given board
        player (str): given player

    Returns:
        bool: did given player win the game
    """
    if player == 'Blue':
        if board[0, 3] > 0 or (board >= 0).all():
            return True
    
    if player == 'Red':
        if board[8, 3] < 0 or (board <= 0).all():
            return True
    
    return False

def score_rank(rank) -> int:
    if rank == 1:
        return -500
    elif rank == 2:
        return -200
    elif rank == 3:
        return -300
    elif rank == 4:
        return -400
    elif rank == 5:
        return -500
    elif rank == 6:
        return -800
    elif rank == 7:
        return -900
    elif rank == 8:
        return -1000
    elif rank == 1:
        return 500
    elif rank == 2:
        return 200
    elif rank == 3:
        return 300
    elif rank == 4:
        return 400
    elif rank == 5:
        return 500
    elif rank == 6:
        return 800
    elif rank == 7:
        return 900
    elif rank == 8:
        return 1000
    else:
        return 0

def score_position(row, col, rank):
    pass

def evaluate(board: list[int, int], row: int, col: int) -> float:
    """Score a given board after move

    Args:
        board (list[int, int]): given board
        row (int): row of moved piece
        col (int): column of moved piece

    Returns:
        float: score
    """
    score = 0
    if is_win(board, 'Red' if board[row, col] < 0 else 'Blue'):
        score += 9999
    else:
        for row in range(9):
            for col in range(7):
                if board[row, col] != 0:
                    score += score_rank(board[row, col])
    
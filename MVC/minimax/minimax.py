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
    
    2: [[8,8,8,0,8,8,8], 
        [13,10,8,8,8,8,8],
        [10,10,10,8,8,8,8],
        [10,0,0,8,0,0,8],
        [10,0,0,8,0,0,8],
        [10,0,0,10,0,0,8],
        [10,11,11,15,11,11,10],
        [11,11,15,50,13,11,11],
        [11,15,50,9999,50,15,11]],
    
    3: [[8,12,12,0,8,8,8],
        [8,12,13,8,8,8,8],
        [8,8,10,8,8,8,8],
        [8,0,0,8,0,0,8],
        [8,0,0,8,0,0,8],
        [9,0,0,10,0,0,9],
        [10,11,15,11,10,9],
        [10,11,15,50,15,11,10],
        [11,15,50,9999, 50,15,11]],
    
    4: [[8,8,8,0,12,12,8],
        [8,8,8,8,13,10,8],
        [8,8,8,8,8,8,8],
        [8,0,0,8,0,0,8],
        [8,0,0,8,0,0,8],
        [9,0,0,10,0,0,9],
        [10,11,15,50,12,11,10],
        [11,15,50,9999, 50,15,11]],
    
    5: [[9,9,9,0,9,9,9],
        [9,9,9,9,9,9,9],
        [9,9,9,10,10,9,9],
        [10,0,0,13,0,0,10],
        [11,0,0,14,0,0,11],
        [12,0,0,15,0,0,12],
        [13,13,14,15,14,13,13],
        [13,14,15,50,15,14,13],
        [14,15,50,9999, 50,15,14]
        ],
    
    6: [[10,12,12,0,12,12,10],
        [12,14,12,12,12,12,12],
        [14,16,16,14,16,16,14],
        [15,0,0,15,0,0,15],
        [15,0,0,15,0,0,15],
        [15,0,0,15,0,0,15],
        [18,20,20,30,20,20,18],
        [25,25,30,50,30,25,25],
        [25,30,50,9999,50,30,25]],
    
    7: [[10,12,12,0,12,12,10],
        [12,14,12,12,12,12,12],
        [14,16,16,14,16,16,14],
        [15,0,0,15,0,0,15],
        [15,0,0,15,0,0,15],
        [15,0,0,15,0,0,15],
        [18,20,20,30,20,20,18],
        [25,25,30,50,30,25,25],
        [25,30,50,9999,50,30,25]],
    
    8: [[11,11,11,0,11,11,11],
        [11,11,11,11,11,11,11],
        [10,15,14,14,14,14,12],
        [12,0,0,12,0,0,12],
        [14,0,0,14,0,0,14],
        [16,0,0,16,0,0,16],
        [18,20,20,30,20,20,18],
        [25,25,30,50,30,25,25],
        [25,30,50,9999,50,30,25]]
    
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
    """Returns the score given to each piece on the AI's side and on the opponent's side.

    Args:
        rank (int): rank to score.

    Returns:
        int: score given.
    """
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
    """Returns a score of a specific piece given its position on the board

    Args:
        row (int): row of current piece
        col ([type]): col of current piece
        rank ([type]): rank of current piece

    Returns:
        int: given score.
    """
    return RANK_DEVELOPMENT[rank][row][col]

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
                    if board[row, col] < 0:
                        score += score_position(row, col, abs(board[row, col]))
                    elif board[row, col] > 0:
                        score -= score_position(9 - row, col, board[row, col])

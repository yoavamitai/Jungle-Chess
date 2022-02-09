
COORDINATES = tuple[int, int]


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

    def __str__(self) -> str:
        return f'start: {self.start}, target: {self.target}'

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
        
        # Move piece
        tmp = board[self.start[0], self.start[1]]
        board[self.start[0], self.start[1]] = 0
        board[self.target[0], self.target[1]] = tmp
    
    def revert(self, board) -> None:
        """Revert a move done on a given board.

        Args:
            board (list[int, int]): given game board
        """
        
        
        # Revert piece Movement
        tmp = board[self.start[0], self.start[1]]
        board[self.start[0], self.start[1]] = board[self.target[0], self.target[1]]
        board[self.target[0], self.target[1]] = tmp
        
        # Revert capture
        if self.is_capturing:
            board[self.target[0], self.target[1]] = self.captured
          

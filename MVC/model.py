import numpy as np
from assets.consts import Consts
class Model:
    def __init__(self) -> None:
        board = [[-7, 0, 0, 0, 0, 0, -6],
                 [0,-4, 0, 0, 0, -2, 0],
                 [-1, 0, -5, 0, -3, 0, -8],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [8, 0, 3, 0, 5, 0, 1],
                 [0, 2, 0, 0, 0, 4, 0],
                 [6, 0, 0, 0, 0, 0, 7]]
        self.game_board = np.asarray(board, dtype=int)    # Turn board var into a numpy ndarray
    
    def is_outside_r_edge(self, pos_x: int):
        """Checks if position X is outside the right edge of the board

        Args:
            pos_x (int): Position X to check

        Returns:
            bool: is outside the right edge of the board.
        """
        return True if pos_x >= 7 else False
    
    def is_outside_l_edge(self, pos_x: int):
        """Checks if the position Y is outside the upper edge of the board

        Args:
            pos_y (int): Position Y to check.

        Returns:
            bool: Is outside the upper edge of the board
        """
        return True if pos_x < 0 else False
    
    def is_outside_u_edge(self, pos_y: int):
        """Checks if the position Y is outside the upper edge of the board

        Args:
            pos_y (int): Position Y to check.

        Returns:
            bool: Is outside the upper edge of the board
        """
        return True if pos_y < 0 else False
    
    def is_outside_d_edge(self, pos_y: int):
        """Checks if the position Y is outside the bottom edge of the board

        Args:
            pos_y (int): Position Y to check.

        Returns:
            bool: Is outside the bottom edge of the board
        """
        return True if pos_y >= 9 else False
    
    def is_overlapping_own_den(self, pos, rank):
        """Checks if the possible position of a game piece is covering its own den

        Args:
            pos (tuple(int, int)): Possible position of a game piece
            rank (int): Rank of the game piece (Positive for blue player, negative for red player)

        Returns:
            bool: Is covering the position of its own den
        """
        if (rank < 0 and pos == (0, 3)) or (rank > 0 and pos == (8, 3)):
            return True
        
        return False
    
    def is_self_rank_higher(self, rank_a, rank_b):
        """Compares rank and other_rank to determine if game piece rank_a can eat game piece rank_b

        Args:
            rank (int): Rank of possible eater
            other_rank (int): Rank of eaten

        Returns:
            bool: Can rank eat other_rank
        """
        if (rank_a > 0 and rank_b > 0) or (rank_a < 0 and rank_b < 0):
            return False
        rank_a = abs(rank_a)
        rank_b = abs(rank_b)

        if rank_a == 1 and rank_b in (0, 1, 8):
            return True
        
        if rank_a == 2 and rank_b <= 2:
            return True
        
        if rank_a == 3 and rank_b <= 3:
            return True
        
        if rank_a == 4 and rank_b <= 4:
            return True
        
        if rank_a == 5 and rank_b <= 5:
            return True
        
        if rank_a == 6 and rank_b <= 6:
            return True
        
        if rank_a == 7 and rank_b <= 7:
            return True
        
        if rank_a == 8 and rank_b in (0, 2, 3, 4, 5, 6, 7, 8):
            return True
        
        return False
            
    def get_directions_to_river(self, pos):
        """Generate a list of adjacent directions to the rivers for a given game piece

        Args:
            pos (tuple(int, int)): game piece position

        Returns:
            list[str]: list of directions to rivers.
        """
        directions = []

        # Check if piece is right to the river
        if pos[1] in (3, 6) and 2 < pos[0] < 6:
            directions.append((0, -1))
        
        # check if piece is left to the river
        if pos[1] in (0, 3) and 2 < pos[0] < 6:
            directions.append((0, 1))
        
        # Check if piece is above the river
        if pos[1] in (1, 2, 4, 5) and pos[0] == 2:
            directions.append((1, 0))
        
        # Check if piece is below the river
        if (pos[1] == 1 or pos[1] == 2 or pos[1] == 4 or pos[1] == 5) and pos[0] == 6:
            directions.append((-1, 0))
        
        return directions
    
    def land_logic(self, pos, rank):
        """Movement logic for land-rank game pieces: Cat, Dog, Wolf, Leopard, Elephant.

        Args:
            pos (tuple(int, int)): current position of the game piece
            rank (int): rank of the current game piece.
        """

        directions_to_river = self.get_directions_to_river(pos)
        moves = []
        print(directions_to_river)
        if len(directions_to_river) == 0:
            for dir in Consts.DIRECTIONS:
                if not self.is_outside_r_edge(pos[1] + dir[1]): 
                    if not self. is_outside_l_edge(pos[1] + dir[1]):
                        if not self.is_outside_u_edge(pos[0] + dir[0]):
                            if not self.is_outside_d_edge(pos[0] + dir[0]):
                                if self.is_self_rank_higher(rank, self.game_board[pos[0] + dir[0], pos[1] + dir[1]]):
                                    if not self.is_overlapping_own_den((pos[0] + dir[0], pos[1] + dir[1]), rank):
                                        moves.append((pos[0] + dir[0], pos[1] + dir[1]))
        
        else:
            DIR = Consts.DIRECTIONS.copy()
            for direction in directions_to_river:
                DIR.remove(direction)
            
            for dir in DIR:
                if not self.is_outside_r_edge(pos[1] + dir[1]): 
                    if not self. is_outside_l_edge(pos[1] + dir[1]):
                        if not self.is_outside_u_edge(pos[0] + dir[0]):
                            if not self.is_outside_d_edge(pos[0] + dir[0]):
                                if self.is_self_rank_higher(rank, self.game_board[pos[0] + dir[0], pos[1] + dir[1]]):
                                    if not self.is_overlapping_own_den((pos[0] + dir[0], pos[1] + dir[1]), rank):
                                        moves.append((pos[0] + dir[0], pos[1] + dir[1]))
        
        return moves
    
    def land_river_logic(self, pos, rank):
        moves = []
        for dir in Consts.DIRECTIONS:
            if not self.is_outside_r_edge(pos[1] + dir[1]): 
                    if not self. is_outside_l_edge(pos[1] + dir[1]):
                        if not self.is_outside_u_edge(pos[0] + dir[0]):
                            if not self.is_outside_d_edge(pos[0] + dir[0]):
                                if self.is_self_rank_higher(rank, self.game_board[pos[0] + dir[0], pos[1] + dir[1]]):
                                    if not self.is_overlapping_own_den((pos[0] + dir[0], pos[1] + dir[1]), rank):
                                        moves.append((pos[0] + dir[0], pos[1] + dir[1]))
        
        return moves

    def land_jump_logic(self, pos, rank):
        directions_to_river = self.get_directions_to_river(pos)
        moves = []
        if len(directions_to_river) == 0:
            for dir in Consts.DIRECTIONS:
                if not self.is_outside_r_edge(pos[1] + dir[1]): 
                    if not self. is_outside_l_edge(pos[1] + dir[1]):
                        if not self.is_outside_u_edge(pos[0] + dir[0]):
                            if not self.is_outside_d_edge(pos[0] + dir[0]):
                                if self.is_self_rank_higher(rank, self.game_board[pos[0] + dir[0], pos[1] + dir[1]]):
                                    if not self.is_overlapping_own_den((pos[0] + dir[0], pos[1] + dir[1]), rank):
                                        moves.append((pos[0] + dir[0], pos[1] + dir[1]))
        
        else:
            for dir in directions_to_river:
                if dir == (1, 0):
                    if self.game_board[3, pos[1]] == 0 and self.game_board[4, pos[1]] == 0 and self.game_board[5, pos[1]] == 0:
                        if self.game_board[2, pos[1]] <= rank:
                            moves.append((2, pos[1]))

                if dir == (-1, 0):
                    if self.game_board[3, pos[1]] == 0 and self.game_board[4, pos[1]] == 0 and self.game_board[5, pos[1]] == 0:
                        if self.game_board[6, pos[1]] <= rank:
                            moves.append((6, pos[1]))
                
                if dir == (0, 1):
                    if self.game_board[pos[0], pos[1] - 1] == 0 and self.game_board[pos[0], pos[1] - 2] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[pos[0], pos[1] - 3]):
                            moves.append((pos[0], pos[1] - 3))
                
                if dir == (0, -1):
                    if self.game_board[pos[0], pos[1] + 1] == 0 and self.game_board[pos[0], pos[1] + 2] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[pos[0], pos[1] + 3]):
                            moves.append((pos[0], pos[1] + 3))
        
        return moves

    def get_possible_moves(self, position):
        """returns possible moves of a game piece for a given position.

        Args:
            position (tuple(int, int)): given position.
        """
        
        moves = None      # Generate possible moves
        current_rank = self.game_board[position[0], position[1]]    # Get current rank

        if current_rank == 0:
            return None
        
        elif abs(current_rank) == 1: # Rat
            moves = self.land_river_logic(position, current_rank)
        elif abs(current_rank) == 2: # Cat
            moves = self.land_logic(position, current_rank)
        elif abs(current_rank) == 3: # Dog
            moves = self.land_logic(position, current_rank)
        elif abs(current_rank) == 4: # Wolf
            moves = self.land_logic(position, current_rank)
        elif abs(current_rank) == 5: # Leopard
            moves = self.land_logic(position, current_rank)
        elif abs(current_rank) == 6: # Tiger
            moves = self.land_jump_logic(position, current_rank)
        elif abs(current_rank) == 7: # Lion
            moves = self.land_jump_logic(position, current_rank)
            
        elif abs(current_rank) == 8: # Elephant
            moves = self.land_logic(position, current_rank)
        
        return moves

    def perform_move(self, game_piece, selected_move):
        """Move a piece from original position to selected position.

        Args:
            game_piece (tuple(int, int)): position of the piece to move
            selected_move (tuple(int, int)): position of selected move
        """
        self.game_board[selected_move[0], selected_move[1]] = self.game_board[game_piece[0], game_piece[1]]
        self.game_board[game_piece[0], game_piece[1]] = 0
        
    def undo_move(self, game_piece):
        pass
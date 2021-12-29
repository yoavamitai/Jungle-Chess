import numpy as np

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
    
    def is_adjacent_to_right_edge(self, pos_x):
        """Checks if position X is outside the right edge of the board

        Args:
            pos_x (int): Position X to check.

        Returns:
            bool: Is outside the right edge of the board
        """
        return True if pos_x == 7 else False
    
    def is_adjacent_to_left_edge(self, pos_x):
        """Checks if position X is outside the left edge of the board

        Args:
            pos_x (int): Position X to check.

        Returns:
            bool: Is outside the left edge of the board
        """
        return True if pos_x == -1 else False

    def is_adjacent_to_upper_edge(self, pos_y):
        """Checks if the position Y is outside the upper edge of the board

        Args:
            pos_y (int): Position Y to check.

        Returns:
            bool: Is outside the upper edge of the board
        """
        return True if pos_y == -1 else False
    
    def is_adjacent_to_bottom_edge(self, pos_y):
        """Checks if the position Y is outside the bottom edge of the board

        Args:
            pos_y (int): Position Y to check.

        Returns:
            bool: Is outside the bottom edge of the board
        """
        return True if pos_y == 9 else False
    
    def is_on_own_den(self, pos, rank):
        """Checks if the possible position of a game piece is covering its own den

        Args:
            pos (tuple(int, int)): Possible position of a game piece
            rank (int): Rank of the game piece (Positive for blue player, negative for red player)

        Returns:
            bool: Is covering the position of its own den
        """
        if rank < 0:
            if pos == (3, 0):
                return True
        elif rank > 0:
            if pos == (3, 8):
                return True
        
        return False
    
    def is_self_rank_higher(self, rank, other_rank):
        """Compares rank and other_rank to determine if game piece with rank can eat game piece with other_rank

        Args:
            rank (int): Rank of possible eater
            other_rank (int): Rank of eaten

        Returns:
            bool: Can rank eat other_rank
        """
        rank = abs(rank)
        other_rank = abs(other_rank)
        if rank == 1:
            if other_rank in (0,1, 8):
                return True
        elif rank == 2:
            if other_rank <= 2:
                return True
        elif rank == 3:
            if other_rank <= 3:
                return True
        elif rank == 4:
            if other_rank <= 4:
                return True
        elif rank == 5:
            if other_rank <= 5:
                return True
        elif rank == 6:
            if other_rank <= 6:
                return True
        elif rank == 7:
            if other_rank <= 7:
                return True
        elif rank == 8:
            if other_rank in (0,2,3,4,5,6,7,8):
                return True
        
        return False

    def get_direction_to_river(self, pos):
        directions = []
        
        # Check if piece is right to the river
        if pos[0] in (3, 6) and 2 < pos[1] < 6:
            directions.append('r')
        
        # check if piece is left to the river
        if pos[0] in (0, 3) and 2 < pos[1] < 6:
            directions.append('l')
        
        # Check if piece is above the river
        if pos[0] in (1, 2, 4, 5) and pos[1] == 2:
            directions.append('u')
        
        # Check if piece is below the river
        if pos[0] in (1, 2, 4, 5) and pos[1] == 6:
            directions.append('d')
        
        return directions
    
    def land_logic(self, pos, rank):
        """Movement logic for land-rank game pieces: Cat, Dog, Wolf, Leopard, Elephant

        Args:
            pos (tuple(int, int)): current position of the game piece
            rank (int): rank of the current game piece
        """
        directions_to_river = self.get_direction_to_river(pos)
        directions = [(pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1])]
        if len(directions_to_river) == 0:
            
            for position in directions:
                if self.is_self_rank_higher(rank, self.game_board[position[0], position[1]]) is False:
                    directions.remove(position)
                elif self.is_adjacent_to_right_edge(position[0]) or self.is_adjacent_to_left_edge(position[0]) or \
                    self.is_adjacent_to_bottom_edge(position[1]) or self.is_adjacent_to_upper_edge(position[1]):
                    directions.remove(position)
                elif self.is_on_own_den(position, rank):
                    directions.remove(position)
        
        else:
            for dir in directions_to_river:
                if dir == 'u':
                    directions.remove((pos[0], pos[1] - 1))
                elif dir == 'd':
                    directions.remove((pos[0], pos[1] + 1))
                elif dir == 'l':
                    directions.remove((pos[0] - 1, pos[1]))
                elif dir == 'r':
                    directions.remove((pos[0] + 1, pos[1]))
            
            for position in directions:
                if self.is_self_rank_higher(rank, self.game_board[position[0], position[1]]) is False:
                    directions.remove(position)
                elif self.is_adjacent_to_right_edge(position[0]) or self.is_adjacent_to_left_edge(position[0]) or \
                    self.is_adjacent_to_bottom_edge(position[1]) or self.is_adjacent_to_upper_edge(position[1]):
                    directions.remove(position)
                elif self.is_on_own_den(position, rank):
                    directions.remove(position)
        
        return directions

    def land_jump_logic(self, pos, rank):
        """Movement logic for land-rank game pieces that can jump: Tiger, Lion

        Args:
            pos (tuple(int, int)): current position of the game piece
            rank (int): rank of the current game piece
        """
        directions_to_river = self.get_direction_to_river(pos)
        directions = [(pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1])]
        if len(directions_to_river) == 0:
            for position in directions:
                if self.is_self_rank_higher(rank, self.game_board[position[0], position[1]]) is False:
                    directions.remove(position)
                elif self.is_adjacent_to_right_edge(position[0]) or self.is_adjacent_to_left_edge(position[0]) or \
                    self.is_adjacent_to_bottom_edge(position[1]) or self.is_adjacent_to_upper_edge(position[1]):
                    directions.remove(position)
                elif self.is_on_own_den(position, rank):
                    directions.remove(position)
        
        else:
            for dir in directions_to_river:
                if dir is 'u':
                    directions.remove((pos[0], pos[1] - 1))
                    if self.game_board[pos[0], 3] == 0 and self.game_board[pos[0], 4] == 0 and self.game_board[pos[0], 5] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[pos[0], 2]):
                            directions.append((pos[0], 2))
                
                if dir is 'd':
                    directions.remove((pos[0], pos[1] + 1))
                    if self.game_board[pos[0], 3] == 0 and self.game_board[pos[0], 4] == 0 and self.game_board[pos[0], 5] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[pos[0], 6]):
                            directions.append((pos[0], 6))
                
                if dir is 'r':
                    directions.remove((pos[0] - 1, pos[1]))
                    if self.game_board[pos[0]-1, pos[1]] == 0 and self.game_board[pos[0] - 2, pos[1]] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[pos[0] - 3, pos[1]]):
                            directions.append((pos[0] - 3, pos[1]))
                
                if dir is 'l':
                    directions.remove((pos[0] + 1, pos[1]))
                    if self.game_board[pos[0]+1, pos[1]] == 0 and self.game_board[pos[0] + 12, pos[1]] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[pos[0] + 3, pos[1]]):
                            directions.append((pos[0] + 3, pos[1]))
                
        return directions

    def land_river_logic(self, pos, rank):
        """Movement logic for land-rank game pieces: Rat

        Args:
            pos (tuple(int, int)): current position of the game piece
            rank (int): rank of the current game piece
        """
        directions = [(pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1])]
        
        for position in directions:
            if self.is_self_rank_higher(rank, self.game_board[position[0], position[1]]) is False:
                directions.remove(position)
            
            elif self.is_adjacent_to_right_edge(position[0]) or self.is_adjacent_to_left_edge(position[0]) or \
                    self.is_adjacent_to_bottom_edge(position[1]) or self.is_adjacent_to_upper_edge(position[1]):
                    directions.remove(position)
            elif self.is_on_own_den(position, rank):
                    directions.remove(position)
        
        return directions

    def get_possible_moves(self, position):
        """returns possible moves of a game piece for a given position.

        Args:
            position (tuple(int, int)): given position.
        """
        
        moves = None      # Generate possible moves
        current_rank = self.game_board[position[0], position[1]]    # Get current rank
        
        # Use one of three logic functions for each rank: land_logic, land_jump_logic, land_river_logic.
        
        if current_rank == 0:
            return None     # return None if tile is empty (0 means empty)
        
        elif current_rank == 1: # Rat
            moves = self.land_river_logic(position, current_rank)
        elif current_rank == 2: # Cat
            moves = self.land_logic(position, current_rank)
        elif current_rank == 3: # Dog
            moves = self.land_logic(position, current_rank)
        elif current_rank == 4: # Wolf
            moves = self.land_logic(position, current_rank)
        elif current_rank == 5: # Leopard
            moves = self.land_logic(position, current_rank)
        elif current_rank == 6: # Tiger
            moves = self.land_jump_logic(position, current_rank)
        elif current_rank == 7: # Lion
            moves = self.land_jump_logic(position, current_rank)
        elif current_rank == 8: # Elephant
            moves = self.land_logic(position, current_rank)
        return moves
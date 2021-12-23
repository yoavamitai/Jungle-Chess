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
    
    def check_moves_for_possible_directions(self, position, rank, directions):
        pass
    
    def get_possible_moves(self, position):
        """returns possible moves of a game piece for a given position.

        Args:
            position (tuple(int, int)): given position.
        """
        
        moves = []      # Generate list of possible moves
        current_rank = self.game_board[position[0], position[1]]    # Get current rank
        
        # Match case for every game piece rank.
        match current_rank:
            case 0:
                return None     # return None if tile is empty (0 means empty)
            case 1: # Rat
                if self.game_board[position[0], position[1] - 1] in (0, 8) and position[1] - 1 >= 0:
                    moves.append(tuple(position[0], position[1] - 1))    # Append move up
                
                if self.game_board[position[0], position[1] + 1] in (0, 8) and position[1] < 9:
                    moves.append(tuple(position[0], position[1] + 1))     # Append move down
                
                if self.game_board[position[0] - 1, position[1]] in (0, 8) and position[0] >= 0:
                    moves.append(tuple(position[0] - 1, position[1]))     # Append move left
                
                if self.game_board[position[0] + 1, position[1]] in (0, 8) and position[0] < 7:
                    moves.append(tuple(position[0] + 1, position[1]))     # Append move right
            case 2: # Cat
                pass
            case 3: # Dog
                pass
            case 4: # Wolf
                pass
            case 5: # Leopard
                pass
            case 6: # Tiger
                pass
            case 7: # Lion
                pass
            case 8: # Elephant
                directions = self.get_direction_to_river(position)
                if len(directions) == 0:
                    # Piece is not adjacent to river
                    if self.game_board[position[0], position[1] - 1] != 1 and position[1] - 1 >= 0:
                        moves.append(tuple(position[0], position[1] - 1))   # Append move up
                    
                    if self.game_board[position[0], position[1] + 1] != 1 and position[1] + 1 < 9:
                        moves.append(tuple(position[0], position[1] + 1))   # Append move down
                    
                    if self.game_board[position[0] - 1, position[1]] != 1 and position[0] - 1 >= 0:
                        moves.append(tuple(position[0] - 1, position[1]))   # Append move left
                    
                    if self.game_board[position[0] + 1, position[1]] != 1 and position[0] + 1 < 7:
                        moves.append(tuple(position[0] + 1, position[1]))   # Append move right
                
                else:
                    pass          
                
        
        return moves
    
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
                pass
        
        return moves
    
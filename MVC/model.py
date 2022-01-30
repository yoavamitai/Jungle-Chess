import numpy as np
from assets.consts import Consts
from math import inf
from MVC.minimax.minimax import Move

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
        self.moves = []
        self.selected_game_piece = None
        self.turn = 0
        
        # Minimax Consts
        self.COORDINATES = tuple[int, int]
        self.RANK_DEVELOPMENT = {
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
        self.RANK_SCORE = {
            1: -500,
            2: -200,
            3: -300,
            4: -400,
            5: -500,
            6: -800,
            7: -900,
            8: -1000,
            -1: 500,
            -2: 200,
            -3: 300,
            -4: 400,
            -5: 500,
            -6: 800,
            -7: 900,
            -8: 1000,
        }
    
    def is_outside_r_edge(self, pos_x: int) -> bool:
        """Checks if position X is outside the right edge of the board

        Args:
            pos_x (int): Position X to check

        Returns:
            bool: is outside the right edge of the board.
        """
        return True if pos_x >= 7 else False
    
    def is_outside_l_edge(self, pos_x: int) -> bool:
        """Checks if the position Y is outside the upper edge of the board

        Args:
            pos_y (int): Position Y to check.

        Returns:
            bool: Is outside the upper edge of the board
        """
        return True if pos_x < 0 else False
    
    def is_outside_u_edge(self, pos_y: int) -> bool:
        """Checks if the position Y is outside the upper edge of the board

        Args:
            pos_y (int): Position Y to check.

        Returns:
            bool: Is outside the upper edge of the board
        """
        return True if pos_y < 0 else False
    
    def is_outside_d_edge(self, pos_y: int) -> bool:
        """Checks if the position Y is outside the bottom edge of the board

        Args:
            pos_y (int): Position Y to check.

        Returns:
            bool: Is outside the bottom edge of the board
        """
        return True if pos_y >= 9 else False
    
    def is_overlapping_own_den(self, pos, rank: int) -> bool:
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
    
    def is_self_rank_higher(self, rank_a: int, rank_b: int) -> bool:
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
    
    def land_logic(self, pos, rank: int):
        """Movement logic for land-rank game pieces: Cat, Dog, Wolf, Leopard, Elephant.

        Args:
            pos (tuple(int, int)): current position of the game piece
            rank (int): rank of the current game piece.
        """

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
    
    def land_river_logic(self, pos, rank: int):
        """Movement logic for land-river game pieces: Rat.

        Args:
            pos (tuple(int, int)): current position of the game piece
            rank (int): rank of the current game piece.
        """
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

    def land_jump_logic(self, pos, rank: int):
        """Movement logic for land-jump game pieces: Tiger, Lion

        Args:
            pos (tuple(int, int)): current position of the game piece
            rank (int): rank of the current game piece.
        """
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
                if dir == (-1, 0):
                    if self.game_board[3, pos[1]] == 0 and self.game_board[4, pos[1]] == 0 and self.game_board[5, pos[1]] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[2, pos[1]]):
                            moves.append((2, pos[1]))
                    if self.is_self_rank_higher(rank, self.game_board[pos[0], pos[1] - 1]):
                        moves.append((pos[0], pos[1] - 1))
                    
                    if self.is_self_rank_higher(rank, self.game_board[pos[0], pos[1] + 1]):
                        moves.append((pos[0], pos[1] + 1))
                    
                    if self.is_self_rank_higher(rank, self.game_board[pos[0] + 1, pos[1]]):
                        moves.append((pos[0] + 1, pos[1]))
                    

                if dir == (1, 0):
                    if self.game_board[3, pos[1]] == 0 and self.game_board[4, pos[1]] == 0 and self.game_board[5, pos[1]] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[6, pos[1]]):
                            moves.append((6, pos[1]))
                    
                    if self.is_self_rank_higher(rank, self.game_board[pos[0], pos[1] - 1]):
                        moves.append((pos[0], pos[1] - 1))
                    
                    if self.is_self_rank_higher(rank, self.game_board[pos[0], pos[1] + 1]):
                        moves.append((pos[0], pos[1] + 1))
                    
                    if self.is_self_rank_higher(rank, self.game_board[pos[0] - 1, pos[1]]):
                        moves.append((pos[0] - 1, pos[1]))
                
                if dir == (0, -1):
                    if self.game_board[pos[0], pos[1] - 1] == 0 and self.game_board[pos[0], pos[1] - 2] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[pos[0], pos[1] - 3]):
                            moves.append((pos[0], pos[1] - 3))
                    
                    if self.is_self_rank_higher(rank, self.game_board[pos[0] - 1, pos[1]]):
                        moves.append((pos[0] - 1, pos[1]))
                    
                    if self.is_self_rank_higher(rank, self.game_board[pos[0] + 1, pos[1]]):
                        moves.append((pos[0] + 1, pos[1]))
                    
                
                if dir == (0, 1):
                    if self.game_board[pos[0], pos[1] + 1] == 0 and self.game_board[pos[0], pos[1] + 2] == 0:
                        if self.is_self_rank_higher(rank, self.game_board[pos[0], pos[1] + 3]):
                            moves.append((pos[0], pos[1] + 3))
                    
                    if self.is_self_rank_higher(rank, self.game_board[pos[0] - 1, pos[1]]):
                        moves.append((pos[0] - 1, pos[1]))
                    
                    if self.is_self_rank_higher(rank, self.game_board[pos[0] + 1, pos[1]]):
                        moves.append((pos[0] + 1, pos[1]))
        
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

    def is_choosing_current_move(self, pos) -> bool:
        """Checks if selected position is in current moves list

        Args:
            pos (tuple(int, int)): Selected position

        Returns:
            bool: answer of the query.
        """
        return True if pos in self.moves and self.selected_game_piece is not None else False
    
    def is_selecting_valid_game_piece(self, pos) -> bool:
        """Check if player is clicking on a valid game piece and not on the opponent's pieces or an empty tile.

        Args:
            pos (tuple(int, int)): selected position

        Returns:
            bool: answer of query.
        """
        return True if (self.game_board[pos[0], pos[1]] > 0 and self.turn == 0) or (self.game_board[pos[0], pos[1]] < 0 and self.turn == 1) else False
    
    def perform_move(self, start_place, selected_move) -> None:
        """Move a piece from original position to selected position.

        Args:
            game_piece (tuple(int, int)): position of the piece to move
            selected_move (tuple(int, int)): position of selected move
        """
        self.game_board[selected_move[0], selected_move[1]] = self.game_board[start_place[0], start_place[1]]
        self.game_board[start_place[0], start_place[1]] = 0
        
    def switch_turn(self) -> None:
        """Switch turn from 0 (Blue) to 1 (Red) and vice versa.
        """
        self.turn = 0 if self.turn == 1 else 1

    def is_win(self):
        """Checks if there is a winner, according to the rules. 

        Returns:
            tuple(bool, str): tuple which contains bool if there is a win and a str which says which player won.
        """
        winning_player = ''
        is_win = False
        # Check win for blue player
        if self.game_board[0, 3] > 0 or (self.game_board >= 0).all():
            print('blue win')
            is_win = True
            winning_player = 'Blue'
            
        
        # Check win for red player
        if self.game_board[8, 3] < 0 or (self.game_board <= 0).all():
            print('red win')
            is_win = True
            winning_player = 'Red'
        
        return (is_win, winning_player)
    
    def reset(self) -> None:
        """Resets model to its initial state.
        """
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
        self.moves = []
        self.selected_game_piece = None
        self.turn = 0
    
    def get_available_pieces(self):
        pieces = []
        for i in range(9):
            for j in range(7):
                if self.game_board[i, j] < 0:
                    pieces.append((i,j))
        return pieces
    
    # Minimax
    
    def is_win_for_player(self, board, player) -> bool:
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

    def score_rank(self, rank) -> int:
        """Returns the score given to each piece on the AI's side and on the opponent's side.

        Args:
            rank (int): rank to score.

        Returns:
            int: score given.
        """
        return self.RANK_SCORE[rank]

    def score_position(self, row, col, rank):
        """Returns a score of a specific piece given its position on the board

        Args:
            row (int): row of current piece
            col ([type]): col of current piece
            rank ([type]): rank of current piece

        Returns:
            int: given score.
        """
        
        #print(self.RANK_DEVELOPMENT[rank])
        return self.RANK_DEVELOPMENT[rank][row][col]

    def evaluate(self, board: list[int, int], color) -> float:
        """Score a given board after move

        Args:
            board (list[int, int]): given board
            row (int): row of moved piece
            col (int): column of moved piece

        Returns:
            float: score
        """
        score = 0
        if self.is_win_for_player(board, color):
            score += 9999
        else:
            for row in range(9):
                for col in range(7):
                    if board[row, col] != 0:
                        score += self.score_rank(board[row, col])
                        if board[row, col] < 0:
                            score += self.score_position(row, col, abs(board[row, col]))
                        elif board[row, col] > 0:
                            score -= self.score_position(9 - row, col, board[row, col])
        
        return score

    def get_all_possible_moves(self, board, color):
        moves = []
        for row in range(9):
            for col in range(7):
                if color == 'Red' and board[row, col] < 0:
                    targets = self.get_possible_moves((row, col))
                    for target in targets:
                        moves.append(Move((row, col), target))
                elif color == 'Blue' and board[row, col] > 0:
                    targets = self.get_possible_moves((row, col))
                    for target in targets:
                        moves.append(Move((row, col), target))
        return moves
                
    def next_color(self, color):
        return 'Blue' if color is 'Red' else 'Red'
    
    def max_play(self, board, color, moves, depth, alpha, beta):
        if self.is_win_for_player(board,color) or self.is_win_for_player(board, self.next_color(color)) or depth == 0:
            return self.evaluate(board, color)
        
        best_score = -inf
        
        for move in moves:
            move.perform(board)
            
            next_moves = self.get_all_possible_moves(board, color)
            
            score = self.min_play(board, self.next_color(color), next_moves, depth - 1, alpha, beta)
            
            move.revert(board)
            print(f'score {type(score)}  best_score {type(best_score)}')
            if score > best_score:
                best_score = score
            if best_score > alpha:
                alpha = best_score
            
            if beta <= alpha:
                break
            
            return best_score
        
    def min_play(self,board, color, moves, depth, alpha, beta):
        if self.is_win_for_player(board, 'Blue') or self.is_win_for_player(board, 'Red') or depth == 0:
            return self.evaluate(board, self.next_color(color))
        
        best_score = inf
        for move in moves:
            move.perform(board)
            
            next_moves = self.get_all_possible_moves(board, color)
            
            score = self.max_play(board, self.next_color(color), next_moves, depth - 1, alpha, beta)
            
            move.revert(board)
            
            if score < best_score:
                best_score = score
            
            if best_score < beta:
                beta = best_score
            
            if beta <= alpha:
                break
            
            return best_score        
        
    def minimax(self, board, color):
        """Minimax algorithm

        Args:
            board (list(int, int)): board to perform move on
            color (str): color of the player

        Returns:
            Move: selected move
        """
        moves: list(Move) = self.get_all_possible_moves(board, color)
        if len(moves) == 0:
            return ()
        
        best_move = moves[0]
        best_score = -inf
        
        depth = 2
        
        if len(moves) > 1:
            for move in moves:
                move.perform(board)
                
                next_moves = self.get_all_possible_moves(board, color)
                
                score = self.min_play(board, self.next_color(color), next_moves, depth, -inf, inf)
                
                move.revert(board)
                
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move
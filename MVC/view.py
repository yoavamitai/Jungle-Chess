from __future__ import annotations
import numpy as np
import pygame as pg
from pygame import time
from assets.button import Button
import time
from assets.consts import Consts
import numpy as np


class View:
    def __init__(self) -> None:
        """Init view component"""

        pg.init()
        self.clock: pg.time.Clock = pg.time.Clock()    # Init Clock
        self.display = pg.display.set_mode((1000, 550), 0, 32)    # Initiate display

        pg.display.update()    # Update display
        time.sleep(0.01)
        self.display.fill((235,235,235))    # Fill display in light-grey color

        self.close_button: Button = Button("#B8C6DB", 20, 30, 75, 45, 
                                   border_radius=50, text='close', font=Consts.button_font)    # Init close button
        
        self.message: str = "Blue player's turn"
        pg.event.set_blocked([pg.MOUSEMOTION, pg.FINGERUP])
        
            
    def draw_board(self, pieces: np.ndarray) -> None:
        """Draw the board tiles and the pieces on the board

        Args:
            pieces (ndarray): 2D array representing game pieces and their place on the board
        """
        pg.display.update()     # Update display
        self.close_button.draw(self.display)    # Draw the close button

        # Draw borad
        width = Consts.COLS * Consts.BLOCK_SIZE + (Consts.COLS - 1) * Consts.GAP    # Width of the actual board, NOT THE SCREEN
        height = Consts.ROWS * Consts.BLOCK_SIZE + (Consts.ROWS - 1) * Consts.GAP   # Height of the actual board, NOT THE SCREEN

        starting_x = 1000 * .5 - width * .5     # X position that should be the starting position of the board
        starting_y = 550 * .5 - height * .5     # Y position that should be the starting position of the board

        # For loop to draw board tiles, using variables initiated above
        for j in range(Consts.ROWS):
            y = starting_y + j * (Consts.BLOCK_SIZE + Consts.GAP)   # Current Y position
            for i in range(Consts.COLS):
                x = starting_x + i * (Consts.BLOCK_SIZE + Consts.GAP)   # Current X position
                pg.draw.rect(self.display, 
                self.choose_tile_color(i, j), 
                (x, y, Consts.BLOCK_SIZE, Consts.BLOCK_SIZE), border_radius= 10)    # Draw tile
        
        
        # Draw game pieces
        for j in range(len(pieces)):
            y = starting_y + j * (Consts.BLOCK_SIZE + Consts.GAP)   # Calculate piece y position
            for i in range(len(pieces[j])):
                x = starting_x + i * (Consts.BLOCK_SIZE + Consts.GAP)   # calculate piece x position
                if pieces[j, i] != 0:   # check if element in array is not null (null == 0), but a game piece
                    # draw game piece circle
                    piece = pg.draw.circle(self.display,
                                   (208, 0, 0) if pieces[j,i] < 0 else (0, 180, 216),
                                   (x + Consts.BLOCK_SIZE // 2, y + Consts.BLOCK_SIZE // 2), Consts.BLOCK_SIZE // 2.25)     # Draw tile
                    
                    piece_text = Consts.button_font.render(str(abs(pieces[j, i])), True, (235, 235, 235)) # render game piece text
                    self.display.blit(piece_text, piece_text.get_rect(center=piece.center)) # blit game piece text to the center of the piece circle            

    def choose_tile_color(self, i: float, j: float) -> tuple[int, int, int]:
        """choose tile color based on its position

        Args:
            i (float): Tile's column
            j (float): Tile's Row

        Returns:
            color[int, int, int]: chosen tile color
        """
        #Den Color
        if i == 3 and (j == 0 or j == Consts.ROWS - 1):
            return Consts.den_color
        
        #Trap Color
        if ((i == 2 or i == 4) and (j == 0 or j == Consts.ROWS - 1)) or \
            ((i == Consts.COLS // 2) and (j == 1 or j == Consts.ROWS - 2)):
            return Consts.trap_color
        
        #River Color
        if (i % 3 != 0) and (j > 2 and j < 6):
            return Consts.river_color
        
        return Consts.grass_color

    def mouse_to_board(self, pos: tuple(int, int)) -> tuple(int, int):
        """Convert mouse position of type tuple(x, y) to tuple(column, row) on board.
        if the mouse click position is not on the board, return None.

        Args:
            pos (tuple(int, int)): mouse position on screen

        Returns:
            tuple(int, int): position of mouse on the board, or None if the mouse is not on the board.
        """
        width = Consts.COLS * Consts.BLOCK_SIZE + (Consts.COLS - 1) * Consts.GAP    # Board width  
        height = Consts.ROWS * Consts.BLOCK_SIZE + (Consts.ROWS - 1) * Consts.GAP   # Board height 

        starting_x = 1000 * .5 - width * .5     # Board starting X position
        starting_y = 550 * .5 - height * .5     # Board starting Y position

        x = (pos[0] - starting_x) / (Consts.BLOCK_SIZE + Consts.GAP)    # Board X position (column)
        y = (pos[1] - starting_y) / (Consts.BLOCK_SIZE + Consts.GAP)    # Board Y position (row)

        
        # Check if the mouse position is outside the board
        if x < 0 or y < 0:
            return (-1, -1)
        
        if x > (Consts.COLS) or y > (Consts.ROWS):
            return (-1, -1)
        
        return (int(x),int(y))
    
    def draw_possible_moves(self, moves: list(tuple(int, int))) -> None:
        """Draw currently possible moves for selected game piece.

        Args:
            moves (list[tuple(int, int)]): list of current possible moves
        """
        if moves is None:
            return None
        width = Consts.COLS * Consts.BLOCK_SIZE + (Consts.COLS - 1) * Consts.GAP    # Board width  
        height = Consts.ROWS * Consts.BLOCK_SIZE + (Consts.ROWS - 1) * Consts.GAP   # Board height 

        starting_x = 1000 * .5 - width * .5
        starting_y = 550 * .5 - height * .5
        
        for move in moves:
            x_pos = move[1] * (Consts.BLOCK_SIZE + Consts.GAP) + starting_x + (Consts.BLOCK_SIZE * .25)
            y_pos = move[0] * (Consts.BLOCK_SIZE + Consts.GAP) + starting_y + (Consts.BLOCK_SIZE * .25)
            
            pg.draw.rect(self.display, (235,222,52,50),(x_pos, y_pos, 30, 30), border_radius=10)
    
    def switch_turn(self, turn: int) -> None:
        """Switch the message based on the current turn.

        Args:
            turn (int): Current turn.
        """
        self.message = "Blue player's turn" if turn == 0 else "Red player's turn"
    
    def draw_status(self) -> None:
        """Draw the current turn status.
        """
        pg.draw.rect(self.display, (235, 235, 235), (20, 400, 250, 75))
        message = Consts.sub_title_font.render(self.message, True, 10)
        self.display.blit(message, (20, 420))
    
    def draw_win_message(self, player) -> None:
        """Draw the winning player to the screen.

        Args:
            player (str): Color of winning player.
        """
        color = (37, 154, 232) if player == "Blue" else (232, 60, 37)       # Choose the color of the winning player
        length = 300        # Size of the dialog.
        pg.draw.rect(self.display, color, ((500 - (length / 2), 275 - (length / 2)), (length, length)), border_radius = 25)     # Draw message background
        message = Consts.message_font.render(f'{player} player won!', True, (235, 235, 235))    # Render message content
        message_rect = message.get_rect(center=(500, 175))      # Set message position
        self.display.blit(message, message_rect)        # Draw message content
        play_again_button = Button('#d4d4d4', 362, 230, 275, 70, 30, 'Play Again', font=Consts.button_font)         # Create play again button, which resets the game
        main_menu_button = Button('#d4d4d4',362, 340, 275, 70, 30, 'Return to Main Menu', font=Consts.button_font)  # Create return to main menu button
        main_menu_button.draw(self.display) # Draw main menu button
        play_again_button.draw(self.display)   # Draw play again button
        
        return play_again_button, main_menu_button      # Return refrences to both buttons.
            

    def reset(self):
        """Reset the view component to its initial state.
        """
        self.display = pg.display.set_mode((1000, 550), 0, 32)    # Initiate display

        pg.display.update()    # Update display
        time.sleep(0.01)
        self.display.fill((235,235,235))    # Fill display in light-grey color

        self.close_button: Button = Button("#B8C6DB", 20, 30, 75, 45, 
                                   border_radius=50, text='close', font=Consts.button_font)    # Init close button
        
        self.message: str = "Blue player's turn"    
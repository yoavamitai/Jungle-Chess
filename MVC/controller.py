from MVC.model import Model
from MVC.view import View
import pygame as pg
from assets.consts import Consts
import numpy as np

class Controller:
    def __init__(self, use_pve: bool) -> None:
        """Initiate the Controller component

        Args:
            use_pve (bool): should game use PvE logic or PvE logic
        """
        self.model: Model = Model()    
        self.view: View = View()      
        self.use_pve = use_pve  # Should the game be played as a Player v AI (true), or Player v Player (false)

        pg.event.set_blocked([pg.MOUSEMOTION, pg.FINGERUP])
        self.main_loop()        # Call for main loop
    
    def main_loop(self):
        """Main game loop
        """
        while True:
            if self.use_pve:    # Should use a PvE game logic or PvP game logic
                self.pve_game_loop(self.model.turn)   # Call for PvE game logic
            else:
                self.pvp_game_loop(self.model.turn)   # Call for PvP game logic
                       
    def pve_game_loop(self, turn: int):
        """PvE game logic

        Args:
            turn (int): turn for blue player (0) or red player (1)
        """
        self.view.draw_status()
        if turn == 0:
            # Turn for blue player
            for event in pg.event.get():
                ev_type = event.type    # Get event type
                self.view.draw_board(self.model.game_board)    # Draw the board
                self.handle(ev_type)    # Handle event
                
        if turn == 1:
            # Turn for red player
            self.view.draw_board(self.model.game_board)     # Draw the board
            selected_move = self.model.find_best_move()
            self.model.selected_game_piece = selected_move.start
            #avail_moves = self.model.get_possible_moves(self.model.selected_game_piece)
            move = selected_move.target
            self.turn_logic_ai(move[0], move[1])

    def pvp_game_loop(self, turn: int):
        self.view.draw_status()
        if turn == 0:
            # Turn for blue player
            for event in pg.event.get():
                ev_type = event.type    # Get event type
                self.view.draw_board(self.model.game_board)    # Draw the board
                self.handle(ev_type)    # Handle event
                
        if turn == 1:
            # Turn for red player
            for event in pg.event.get():
                ev_type = event.type    # Get event type
                self.view.draw_board(self.model.game_board)     # Draw the board
                self.handle(ev_type)    # handle even

    def turn_logic_human(self, row, col):
        """Turn logic for human players

        Args:
            row (int): selected row
            col (int): selected col
        """
        if self.model.is_choosing_current_move((row, col)):     # Check if selected move is in the current move list
                        self.model.perform_move(self.model.selected_game_piece, (row, col))     # Perform move in the model.
                        self.view.draw_board(self.model.game_board)     # Draw updated board to screen using the view component
                        self.model.moves = []       # Reset current moves list
                        self.model.selected_game_piece = None       # Reset selected game piece
                        is_win = self.model.is_win()        # Get win data.
                        if is_win[0]:       # Check if there is a win
                            play_again_button, main_menu_button = self.view.draw_win_message(is_win[1])         # Draw win message a retrieve refrences to both buttons.
                            self.view.draw_board(self.model.game_board)         # Draw updated board
                            while True:     # Create new event listener for new buttons.
                                for event in pg.event.get():
                                    if event.type == pg.MOUSEBUTTONDOWN:
                                        if play_again_button.is_over(pg.mouse.get_pos()):
                                            self.reset_game()
                                            
                                        elif main_menu_button.is_over(pg.mouse.get_pos()):
                                            pass
                                    if event == pg.QUIT:
                                        pg.quit()
                                        quit()
                        else:       # If there is no winner
                            self.model.switch_turn()        # Switch the turn, for Blue to Red and vice versa
                            self.view.switch_turn(self.model.turn)      # Switch the turn message in the view component               
        else:       # If choosing a tile which is not in the current moves list
            if self.model.is_selecting_valid_game_piece((row, col)):    # And choosing another valid game piece
                self.model.moves = self.model.get_possible_moves((row, col))    # Update current moves list
                print(f'possible moves: {self.model.moves}')    # Print new moves list
                self.model.selected_game_piece = (row, col)     # Update selected game piece in the model component.
                self.view.draw_possible_moves(self.model.moves) # Draw new moves to the board using the view component            
    
    def turn_logic_ai(self, row: int, col: int) -> None:
        """Turn Logic for AI Player.

        Args:
            row (int): selected row for move
            col (int): selected col for move
        """
        self.model.perform_move(self.model.selected_game_piece, (row, col)) # Perform selected move in the model component

        self.view.draw_board(self.model.game_board) # Update the board in the view component
        self.model.moves = [] # Reset the available moves list
        self.model.selected_game_piece = None # Reset the selected game piece
        is_win = self.model.is_win() # Check if there is a win and store the data
        if is_win[0]:       # Check if there is a win
            play_again_button, quit_button = self.view.draw_win_message(is_win[1])         # Draw win message a retrieve refrences to both buttons.
            self.view.draw_board(self.model.game_board)         # Draw updated board
            while True:     # Create new event listener for new buttons.
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if play_again_button.is_over(pg.mouse.get_pos()):
                            self.reset_game()
                            
                        elif quit_button.is_over(pg.mouse.get_pos()):
                            pg.quit()
                            quit()
                    if event == pg.QUIT:
                        pg.quit()
                        quit()
        else:       # If there is no winner
            self.model.switch_turn()        # Switch the turn, for Blue to Red and vice versa
            self.view.switch_turn(self.model.turn)      # Switch the turn message in the view component     
    
              
    def handle(self, event):
        """handle events from pygame

        Args:
            event ([type]): event type
        """
        if event is pg.QUIT:
            # Handle OS quit button click
            pg.quit()
            quit()
        
        elif event in (pg.MOUSEBUTTONDOWN, pg.FINGERDOWN):
            mouse_loc = pg.mouse.get_pos() # Get mouse position
            if self.view.close_button.is_over(mouse_loc):
                # Handle game quit button click
                self.model.save_cache()
                pg.quit()
                quit()
            else:
                # Handle click on screen, not on quit button
                col, row = self.view.mouse_to_board(mouse_loc) # Get row and column selected
                if col == row == -1:
                    pass
                else:
                    self.turn_logic_human(row, col) # Run the Human Player turn logic using selected rowand col from click.
                            
    def reset_game(self) -> None:
        """Resets the game to its initial state and restarts the game loop.
        """
        self.model.reset() # Reset Model component
        self.view.reset()  # Reset View Component
        self.main_loop()   # Restart controller loop
    

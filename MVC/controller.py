from MVC.model import Model
from MVC.view import View
import time
import pygame as pg
from assets.consts import Consts


class Controller:
    def __init__(self, use_pve: bool) -> None:
        """Initiate the Controller component

        Args:
            use_pve (bool): should game use PvE logic or PvE logic
        """
        self.model: Model = Model()    
        self.view: View = View()      
        self.use_pve = use_pve  # Should the game be played as a Player v AI (true), or Player v Player (false)

        pg.event.set_blocked([pg.MOUSEMOTION])
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
        if turn == 0:
            # turn for human player
            for event in pg.event.get():
                ev_type = event.type
                self.view.draw_board(self.model.game_board)     # Draw the board post-turn change
                self.handle(ev_type)    # Handle event
                
                

        elif turn == 1:
            # turn for AI
            time.sleep(0.2)
            # TODO: perform move
        
        #pg.display.update()
        self.view.clock.tick(Consts.FPS)

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
                ev_type = event.type
                self.view.draw_board(self.model.game_board)
                self.handle(ev_type) 
     
    def handle(self, event):
        """handle events from pygame

        Args:
            event ([type]): event type
        """
        if event is pg.QUIT:
            # Handle OS quit button click
            pg.quit()
            quit()
        
        elif event == pg.MOUSEBUTTONDOWN:
            mouse_loc = pg.mouse.get_pos() # Get mouse position
            if self.view.close_button.is_over(mouse_loc):
                # Handle game quit button click
                pg.quit()
                quit()
            else:
                # Handle click on screen, not on quit button
                col, row = self.view.mouse_to_board(mouse_loc) # Get row and column selected
                if col == row == -1:
                    pass
                else:
                    print(f'col: {col}, row: {row}')
                    
                    if self.model.is_choosing_current_move((row, col)):
                        self.model.perform_move(self.model.selected_game_piece, (row, col))
                        self.view.draw_board(self.model.game_board)
                        self.model.moves = []
                        self.model.selected_game_piece = None
                        is_win = self.model.is_win()
                        if is_win[0]:
                            
                            play_again_button, main_menu_button = self.view.draw_win_message(is_win[1])
                            self.view.draw_board(self.model.game_board)
                            while True:
                                for event in pg.event.get():
                                    if event.type == pg.MOUSEBUTTONDOWN:
                                        if play_again_button.is_over(pg.mouse.get_pos()):
                                            self.reset_game()
                                            
                                        elif main_menu_button.is_over(pg.mouse.get_pos()):
                                            pass
                                    if event == pg.QUIT:
                                        pg.quit()
                                        quit()
                        else:
                            self.model.switch_turn()
                            self.view.switch_turn(self.model.turn)                 
                    else:
                        if self.model.is_selecting_valid_game_piece((row, col)):
                            self.model.moves = self.model.get_possible_moves((row, col))
                            print(f'possible moves: {self.model.moves}')
                            self.model.selected_game_piece = (row, col)
                            self.view.draw_possible_moves(self.model.moves)
                            
    def reset_game(self):
        self.model.reset()
        self.view.reset()
        self.main_loop()
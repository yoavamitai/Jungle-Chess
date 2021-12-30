from MVC.model import Model
from MVC.view import View
import time
import pygame as pg

from pygame.event import Event

from assets.consts import Consts


class Controller:
    def __init__(self, use_pve: bool) -> None:
        """Initiate the Controller component

        Args:
            use_pve (bool): should game use PvE logic or PvE logic
        """
        self.model = Model()    
        self.view = View()      
        self.use_pve = use_pve  # Should the game be played as a Player v AI (true), or Player v Player (false)
        self.turn: int = 0      # 0 for blue, 1 for red
        self.main_loop()        # Call for main loop
    
    def main_loop(self):
        """Main game loop
        """
        while True:
            self.view.draw_board(self.model.game_board)     # Draw the board post-turn change
            if self.use_pve:    # Should use a PvE game logic or PvP game logic
                self.pve_game_loop(self.turn)   # Call for PvE game logic
                
    def pve_game_loop(self, turn: int):
        """PvE game logic

        Args:
            turn (int): turn for blue player (0) or red player (1)
        """
        if turn == 0:
            # turn for human player
            for event in pg.event.get():
                ev_type = event.type
                self.handle(ev_type)    # Handle event

        elif turn == 1:
            # turn for AI
            time.sleep(0.2)
            # TODO: perform move
        
        pg.display.update()
        self.view.clock.tick(Consts.FPS)

    
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
                pg.quit
                quit()
            else:
                # Handle click on screen, not on quit button
                col, row = self.view.mouse_to_board(mouse_loc)
                print(f'col: {col}, row: {row}')
                print(self.model.get_possible_moves((row, col)))

    
    

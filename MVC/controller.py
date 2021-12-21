from MVC.model import Model
from MVC.view import View
import time
import pygame as pg

from pygame.event import Event

from assets.consts import Consts


class Controller:
    def __init__(self, use_pve: bool) -> None:
        self.model = Model()
        self.view = View()
        self.use_pve = use_pve
        self.turn: int = 0  # 0 for blue, 1 for red
        self.main_loop()
    
    def main_loop(self):
        self.view.draw_board(self.model.game_board)
        while True:
            if self.use_pve:
                self.pve_game_loop(self.turn)
                
    def pve_game_loop(self, turn: int):
        if turn == 0:
            # turn for human player
            self.view.draw_board(self.model.game_board)

            for event in pg.event.get():
                ev_type = event.type
                self.handle(ev_type)

        elif turn == 1:
            # turn for AI
            self.view.draw_board(self.model.game_board)
            time.sleep(0.2)
            # TODO: perform move
        
        pg.display.update()
        self.view.clock.tick(Consts.FPS)

    
    def handle(self, event):
            pass

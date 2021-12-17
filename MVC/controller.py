from MVC.model import Model
from MVC.view import View
import time
import pygame as pg


class Controller:
    def __init__(self, use_pve: bool) -> None:
        self.model = Model()
        self.view = View()
        self.use_pve = use_pve
        self.main_loop()
    
    def main_loop(self):
        self.view.draw_board(self.model.game_board)
        while True:
            time.sleep(0.01)
            pg.display.update()
            

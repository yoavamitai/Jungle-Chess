from __future__ import annotations

import pygame as pg
from pygame import time
from assets.button import Button
import time
from assets.consts import Consts

class View:
    def __init__(self) -> None:
        """Init view component"""

        pg.init()
        self.clock = pg.time.Clock() # Init Clock
        self.display = pg.display.set_mode((1200, 750), 0, 32)

        pg.display.update()
        time.sleep(0.01)
        self.display.fill((235,235,235))


        #init view consts
        self.ROWS = 9
        self.COLS = 7
        self.BLOCK_SIZE = 65
        self.GAP = 10
        self.main_loop()
    
    def main_loop(self) -> None:
        """Testing inf loop"""
        while True:
            time.sleep(0.1)
            self.draw_board()
            pg.display.update()

    
    def draw_board(self):
        width = self.COLS * self.BLOCK_SIZE + (self.COLS - 1) * self.GAP
        height = self.ROWS * self.BLOCK_SIZE + (self.ROWS - 1) * self.GAP

        starting_x = 1200 * .5 - width * .5
        starting_y = 750 * .5 - height * .5

        for j in range(self.ROWS):
            y = starting_y + j * (self.BLOCK_SIZE + self.GAP)
            for i in range(self.COLS):
                x = starting_x + i * (self.BLOCK_SIZE + self.GAP)
                pg.draw.rect(self.display, 
                self.choose_block_color(i, j), 
                (x, y, self.BLOCK_SIZE, self.BLOCK_SIZE), border_radius= 10)

    def choose_block_color(self, i: float, j: float) -> tuple[int, int, int]:

        #Den Color
        if i == 3 and (j == 0 or j == self.ROWS - 1):
            return Consts.den_color
        
        #Trap Color
        if ((i == 2 or i == 4) and (j == 0 or j == self.ROWS - 1)) or \
            ((i == self.COLS // 2) and (j == 1 or j == self.ROWS - 2)):
            return Consts.trap_color
        
        #River Color
        if (i % 3 != 0) and (j > 2 and j < 6):
            return Consts.river_color
        
        return Consts.grass_color

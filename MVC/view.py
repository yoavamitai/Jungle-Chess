import pygame as pg
from pygame import time
from assets.button import Button
import time

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
                pg.draw.rect(self.display, (0, 0, 0), (x, y, self.BLOCK_SIZE, self.BLOCK_SIZE), border_radius= 10)
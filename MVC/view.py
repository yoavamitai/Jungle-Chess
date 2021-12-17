from __future__ import annotations
from os import cpu_count
import numpy as np
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
        self.display = pg.display.set_mode((1000, 550), 0, 32)

        pg.display.update()
        time.sleep(0.01)
        self.display.fill((235,235,235))

        self.close_button = Button("#B8C6DB", 20, 30, 75, 45, border_radius=50, text='close', font=Consts.button_font)
        
        #self.main_loop()
        
    
    def main_loop(self) -> None:
        """Testing inf loop"""
        while True:
            time.sleep(0.1)

            self.draw_board()
            
            
    def draw_board(self, pieces):
        pg.display.update()
        self.close_button.draw(self.display)

        # Draw borad
        width = Consts.COLS * Consts.BLOCK_SIZE + (Consts.COLS - 1) * Consts.GAP
        height = Consts.ROWS * Consts.BLOCK_SIZE + (Consts.ROWS - 1) * Consts.GAP

        starting_x = 1000 * .5 - width * .5
        starting_y = 550 * .5 - height * .5

        for j in range(Consts.ROWS):
            y = starting_y + j * (Consts.BLOCK_SIZE + Consts.GAP)
            for i in range(Consts.COLS):
                x = starting_x + i * (Consts.BLOCK_SIZE + Consts.GAP)
                pg.draw.rect(self.display, 
                self.choose_block_color(i, j), 
                (x, y, Consts.BLOCK_SIZE, Consts.BLOCK_SIZE), border_radius= 10)
        
        
        # Draw game pieces
        for j in range(len(pieces)):
            y = starting_y + j * (Consts.BLOCK_SIZE + Consts.GAP)   # calculate piece y position
            for i in range(len(pieces[i])):
                x = starting_x + i * (Consts.BLOCK_SIZE + Consts.GAP)   # calculate piece x position
                if pieces[j, i] != 0:   # check if element in array is not null (null == 0), but a game piece
                    # draw game piece circle
                    piece = pg.draw.circle(self.display,
                                   (208, 0, 0) if pieces[j,i] < 0 else (0, 180, 216),
                                   (x + Consts.BLOCK_SIZE // 2, y + Consts.BLOCK_SIZE // 2), Consts.BLOCK_SIZE // 2.25)
                    
                    piece_text = Consts.button_font.render(str(abs(pieces[j, i])), True, (235, 235, 235)) # render game piece text
                    self.display.blit(piece_text, piece_text.get_rect(center=piece.center)) # blit game piece text to the center of the piece circle
                    

    def choose_block_color(self, i: float, j: float) -> tuple[int, int, int]:

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

import pygame as pg
from button import Button
import time
from consts import Consts
class MainMenu:
    def __init__(self) -> None:
        """Init main menu
        """
        pg.init()

        # Init Clock
        self.clock = pg.time.Clock()

        # Screen Layout
        self.display = pg.display.set_mode((1200, 750), 0, 32)
        self.pvp_button = Button("#B8C6DB", 100, 100, 200, 100, border_radius=10, text="Play PvP", font=Consts.button_font)
        self.pve_button = Button("#B8C6DB", 100, 250, 200, 100, border_radius=10, text="Play PvE", font=Consts.button_font)
        self.instuctions_button = Button("#B8C6DB", 100, 400, 200, 100, border_radius=10, text="Instructions", font=Consts.button_font)
        self.quit_button = Button("#B8C6DB", 100, 550, 200, 100, border_radius=10, text="Quit", font=Consts.button_font)
        self.buttons = [self.pvp_button, self.pve_button, self.instuctions_button, self.quit_button]
        pg.display.update()
        time.sleep(0.01)
        self.display.fill((235, 235, 235))

        for button in self.buttons:
            button.draw(self.display)
        
        self.main_menu_loop()
    
    def main_menu_loop(self) -> None:
        """Main Menu loop
        """
        while True:
            pg.display.update()
            pg.event.get()

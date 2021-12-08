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
        self.pvp_button = Button("#B8C6DB", 60, 150, 200, 100, border_radius=10, text="Play PvP", font=Consts.button_font)
        self.pve_button = Button("#B8C6DB", 60, 300, 200, 100, border_radius=10, text="Play PvE", font=Consts.button_font)
        self.instuctions_button = Button("#B8C6DB", 60, 450, 200, 100, border_radius=10, text="Instructions", font=Consts.button_font)
        self.quit_button = Button("#B8C6DB", 60, 600, 200, 100, border_radius=10, text="Quit", font=Consts.button_font)
        self.buttons = [self.pvp_button, self.pve_button, self.instuctions_button, self.quit_button]
        
        self.texts = [Consts.main_title_font.render('Dou Shou Qi', True, (0,0,0)),
        Consts.sub_title_font.render('Jungle Chess', True, (0,0,0)),
        Consts.label_font.render('by Yoav Amitai', True, (0,0,0))]

        self.text_rects = [self.texts[0].get_rect(center=(200, 50)),
        self.texts[1].get_rect(center=(260, 85)),
        self.texts[2].get_rect(center=(290, 110))]

        
        
        pg.display.update()
        time.sleep(0.01)
        self.display.fill((235, 235, 235))

        for button in self.buttons:
            button.draw(self.display)

        for i in range(3):
            self.display.blit(self.texts[i], self.text_rects[i])
        self.main_menu_loop()
    
    def main_menu_loop(self) -> None:
        """Main Menu loop
        """
        while True:
            pg.display.update()
            pg.event.get()

import pygame as pg
from button import Button
# from screens.instructions import Instructions
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
            pg.display.update()     # Refresh display
            
            for button in self.buttons:
                button.draw(self.display)   # Draw button
            
            pos = pg.mouse.get_pos()    # Get mouse position
            
            for event in pg.event.get():
                """Handle events"""
                ev_type = event.type
                if ev_type == pg.QUIT:      # if event was quit, exit program
                    pg.quit()
                    quit()
                
                elif ev_type == pg.MOUSEBUTTONDOWN:     # if event was mouse button down, handle press
                    if self.buttons[0].is_over(pos):    # Handle press on PvP Button
                        #TODO: handle press on PvP Button
                        pass
                    elif self.buttons[1].is_over(pos):  # Handle press on PvE Button
                        #TODO: handle press on PvE Button
                        pass
                    elif self.buttons[2].is_over(pos):  # Handle press on Instructions Button
                        pg.display.quit()
                        time.sleep(0.2)
                        instructions = Instructions()
                    elif self.buttons[3].is_over(pos):  # Handle press on quit Button
                        pg.quit()
                        quit()
                        
                        
class Instructions:
    def __init__(self) -> None:
        """Init instructions screen"""
        
        pg.init()

        # Init Clock
        self.clock = pg.time.Clock()

        # Screen Layout
        self.display = pg.display.set_mode((1200, 750), 0, 32)
            # Init Buttons
        self.back = Button("#B8C6DB", 20, 30, 45, 45, border_radius=10, text="<", font=Consts.sub_title_font)
            # Init title
        self.title = Consts.main_title_font.render('Instructions', True, (0,0,0))
        self.text_rect = self.title.get_rect(center=(200, 50))

            # Fill screen
        pg.display.update()
        time.sleep(0.01)
        self.display.fill((235, 235, 235))
        
            # Draw Screen components
        self.back.draw(self.display)
        self.display.blit(self.title, self.text_rect)
        
        self.main_menu_loop()
    
    def main_menu_loop(self) -> None:
        """Main Menu loop
        """
        while True:
            pg.display.update()     # Refresh display
            
            
            self.back.draw(self.display)   # Draw button
            
            pos = pg.mouse.get_pos()    # Get mouse position
            
            for event in pg.event.get():
                """Handle events"""
                ev_type = event.type
                if ev_type == pg.QUIT:      # if event was quit, exit program
                    pg.quit()
                    quit()
                
                elif ev_type == pg.MOUSEBUTTONDOWN:     # if event was mouse button down
                    if self.back.is_over(pos):
                        pg.display.quit()
                        time.sleep(0.2)
                        main_menu = MainMenu()
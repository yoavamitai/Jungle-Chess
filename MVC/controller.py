from MVC.model import Model
from MVC.view import View
import time
class Controller:
    def __init__(self, use_pve: bool) -> None:
        self.model = Model()
        self.view = View()
        self.use_pve = use_pve
        self.main_loop()
    
    def main_loop(self):
        while True:
            time.sleep(0.01)
            self.view.draw_board(self.model.board)

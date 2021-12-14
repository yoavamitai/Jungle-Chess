from MVC.model import Model
from MVC.view import View
class Controller:
    def __init__(self, use_pve: bool) -> None:
        self.model = Model()
        self.view = View()
        self.use_pve = use_pve
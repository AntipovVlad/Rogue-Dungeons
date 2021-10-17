from .base_object import *

class Bomb(BaseObject):
    def __init__(self, en_y: int, en_x: int, t_creation) -> None:
        super().__init__(en_y, en_x, 'bomb', 'O')
        self.time = 3
        self.creation = t_creation
    
    def get_time(self):
        return self.creation
    
    def get_live(self) -> None:
        return self.time
    
    def explode(self) -> list:
        return [[self.y - 1, self.x], [self.y + 1, self.x], [self.y, self.x - 1],[self.y, self.x + 1]]


class Explosion(BaseObject):
    def __init__(self, en_y: int, en_x: int, t_creation) -> None:
        super().__init__(en_y, en_x, 'expl', '*')
        self.time = 0.5
        self.creation = t_creation
    
    def get_time(self):
        return self.creation
    
    def get_live(self) -> None:
        return self.time

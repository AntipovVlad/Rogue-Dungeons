from .base_object import *


class Hero(BaseObject):
    def __init__(self, en_y: int, en_x: int) -> None:
        super().__init__(en_y, en_x, 'hero', '@')
        self.max_hp, self.hp = 3, 3
        self.armor = 1
        self.max_bombs, self.bombs = 3, 3
    
    def get_hp(self) -> int:
        return self.hp
    
    def get_max_hp(self) -> int:
        return self.max_hp
    
    def get_bombs(self) -> int:
        return self.bombs
    
    def is_dead(self) -> bool:
        return self.hp < 1
    
    def de_health(self, d=1) -> None:
        self.hp -= d
    
    def de_bombs(self) -> None:
        self.bombs -= 1
    
    def in_bombs(self) -> None:
        self.bombs = min(self.bombs + 1, self.max_bombs)
    
    def set_possintion(self, en_y: int, en_x: int) -> None:
        self.y, self.x = en_y, en_x

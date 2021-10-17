class Hero:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.hp, self.armor = 3, 1
        self.y, self.x = en_y, en_x
        self.skin = '@'
    
    def get_coordinates(self) -> tuple:
        return self.y, self.x
    
    def get_skin(self) -> str:
        return self.skin
    
    def is_dead(self) -> bool:
        return self.hp < 1
    
    def de_health(self, d=1) -> None:
        self.hp -= d
    
    def set_possintion(self, en_y: int, en_x: int) -> None:
        self.y, self.x = en_y, en_x

class Bomb:
    def __init__(self, en_y: int, en_x: int, t_creation) -> None:
        self.y, self.x = en_y, en_x
        self.time = 3
        self.skin = '0'
        self.creation = t_creation
    
    def get_coordinates(self) -> tuple:
        return self.y, self.x
    
    def get_skin(self) -> str:
        return self.skin
    
    def get_time(self):
        return self.creation
    
    def get_live(self) -> None:
        return self.time
    
    def explode(self) -> list:
        return [[self.y - 1, self.x], [self.y + 1, self.x], [self.y, self.x - 1],[self.y, self.x + 1]]


class Explosion:
    def __init__(self, en_y: int, en_x: int, t_creation) -> None:
        self.y, self.x = en_y, en_x
        self.time = 0.5
        self.skin = '*'
        self.creation = t_creation
    
    def get_time(self):
        return self.creation
    
    def get_live(self) -> None:
        return self.time
    
    def get_coordinates(self) -> tuple:
        return self.y, self.x
    
    def get_skin(self) -> str:
        return self.skin

class Hero:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.hp, self.armor = 3, 1
        self.y, self.x = en_y, en_x
    
    def get_coordinates(self) -> tuple:
        return self.y, self.x
    
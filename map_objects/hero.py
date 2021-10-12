class Hero:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.hp = 3
        self.y = en_y
        self.x = en_x
    
    def get_coordinates(self) -> tuple:
        return self.y, self.x
    
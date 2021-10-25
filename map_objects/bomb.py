class Bomb:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.y, self.x = en_y, en_x
        self.time = 500
    
    def explode(self):
        pass


class Explosion:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.y, self.x = en_y, en_x

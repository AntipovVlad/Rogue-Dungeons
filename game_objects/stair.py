class Stair:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.y, self.x = en_y, en_x
        self.skin = 'e'

    def get_skin(self) -> str:
        return self.skin

    def get_coordinates(self) -> tuple:
        return self.y, self.x

class BaseObject:
    def __init__(self, en_y: int, en_x: int, en_type: str, en_skin: str) -> None:
        self.y, self.x = en_y, en_x
        self.type = en_type
        self.skin = en_skin
    
    def get_coordinates(self) -> tuple:
        return self.y, self.x
    
    def get_skin(self) -> str:
        return self.skin

    def get_type(self) -> None:
        return self.type

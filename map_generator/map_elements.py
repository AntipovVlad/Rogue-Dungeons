class Block:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.locked = False
        self.number = 2 ** 16
        self.island = None

        self.y = en_y
        self.x = en_x
    
    def lock_block(self) -> None:
        self.locked = True
    
    def set_number(self, en_number: int) -> None:
        self.number = en_number
    
    def null(self) -> None:
        self.number = 2 ** 16
    
    def is_locked(self) -> bool:
        return self.locked
    
    def is_counted(self) -> bool:
        return self.number != 2 ** 16
    
    def get_number(self) -> int:
        return self.number
    
    def get_island(self) -> object:
        return self.island


class SeaBlock(Block):
    def __init__(self, en_y: int, en_x: int) -> None:
        super().__init__(en_y, en_x)


class GroundBlock(Block):
    def __init__(self, en_y: int, en_x: int, en_island: object, en_beach: bool = False) -> None:
        super().__init__(en_y, en_x)
        self.lock_block()

        self.island = en_island
        self.is_beach = en_beach


class BridgeBlock(Block):
    def __init__(self, en_y: int, en_x: int) -> None:
        super().__init__(en_y, en_x)
        self.lock_block()

class RectangularIsland:
    def __init__(self, coors: list) -> None:
        self.lt_y, self.lt_x = coors[0]
        self.rb_y, self.rb_x = coors[1]
    
    def get_coordinates(self) -> tuple:
        return self.lt_y, self.lt_x, self.rb_y, self.rb_x

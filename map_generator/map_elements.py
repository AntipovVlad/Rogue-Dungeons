class Block:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.changeable = True
        self.counted = False
        
        self.y = en_y
        self.x = en_x
    
    def lock_block(self) -> None:
        self.changeable = False
    
    def is_locked(self) -> bool:
        return self.changeable


class SeaBlock(Block):
    def __init__(self, en_y: int, en_x: int) -> None:
        super().__init__(en_y, en_x)


class GroundBlock(Block):
    def __init__(self, en_y: int, en_x: int, en_island: object) -> None:
        super().__init__(en_y, en_x)
        self.island = en_island


class RectangularIsland:
    def __init__(self, coors: list) -> None:
        self.lt_y, self.lt_x = coors[0]
        self.rb_y, self.rb_x = coors[1]

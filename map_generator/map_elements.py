class Block:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.changeable = True
        self.y = en_y
        self.x = en_x
    
    def lock_block(self):
        self.changeable = False


class SeaBlock(Block):
    def __init__(self, en_y: int, en_x: int) -> None:
        super().__init__(en_y, en_x)


class GroundBlock(Block):
    def __init__(self, en_y: int, en_x: int) -> None:
        super().__init__(en_y, en_x)


class RectangularIsland:
    pass

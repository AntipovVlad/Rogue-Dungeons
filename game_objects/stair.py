from .base_object import *


class Stair(BaseObject):
    def __init__(self, en_y: int, en_x: int) -> None:
        super().__init__(en_y, en_x, 'stair', 'e')

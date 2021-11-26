from .base_object import *

class Box(BaseObject):
    def __init__(self, en_y: int, en_x: int) -> None:
        super().__init__(en_y, en_x, 'box', '▧')

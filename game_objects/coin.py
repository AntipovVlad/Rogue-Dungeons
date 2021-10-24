from .base_object import *
from time import time
# ◎ ◉

class Coin(BaseObject):
    def __init__(self, en_y: int, en_x: int) -> None:
        super().__init__(en_y, en_x, 'coin', '◉')
        self.bl = 0
        self.t = time()
    
    def blink(self):
        if float(time() - self.t) > 0.5:
            self.t = time()
            self.bl = (self.bl + 1) % 2
            self.skin = [chr(int('2460', 16)), chr(int('2776', 16))][self.bl]
        
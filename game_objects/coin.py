from .base_object import *
from time import time


class Coin(BaseObject):
    """
    Class of coin object
    """
    
    def __init__(self, en_y: int, en_x: int) -> None:
        """
        Initial function

        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int

        :rtype: None
        :return: None
        """

        super().__init__(en_y, en_x, 'coin', chr(int('2460', 16)))
        self.bl = 0
        self.t = time()
    
    def blink(self) -> None:
        """
        Makes coin blink

        :rtype: None
        :return: None
        """
        
        if float(time() - self.t) > 0.5:
            self.t = time()
            self.bl = (self.bl + 1) % 2
            self.skin = [chr(int('2460', 16)), chr(int('2776', 16))][self.bl]

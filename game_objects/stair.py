from .base_object import *


class Stair(BaseObject):
    """
    Class of stair object
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
        
        super().__init__(en_y, en_x, 'stair', 'e')

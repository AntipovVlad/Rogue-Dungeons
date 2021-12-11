from .base_object import *

class Bomb(BaseObject):
    """
    Class of bomb object
    """
    
    def __init__(self, en_y: int, en_x: int, t_creation: float) -> None:
        """
        Initial function

        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int
        :param t_creation: time of object creation
        :type t_creation: float

        :rtype: None
        :return: None
        """
        
        super().__init__(en_y, en_x, 'bomb', 'Q')
        self.time = 2
        self.creation = t_creation
    
    def get_time(self) -> float:
        """
        Returns creation time

        :rtype: float
        :return: time
        """
        
        return self.creation
    
    def get_live(self) -> float:
        """
        Returns time of life

        :rtype: float
        :return: time
        """
        
        return self.time
    
    def explode(self) -> list:
        """
        Returns surrounding

        :rtype: list
        :return: array with coordinates
        """
        
        return [[self.y - 1, self.x], [self.y + 1, self.x], [self.y, self.x - 1],[self.y, self.x + 1]]


class Explosion(BaseObject):
    """
    Class of explosion object
    """
    
    def __init__(self, en_y: int, en_x: int, t_creation) -> None:
        """
        Initial function

        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int
        :param t_creation: time of object creation
        :type t_creation: float
        """

        super().__init__(en_y, en_x, 'expl', '*')
        self.time = 0.5
        self.creation = t_creation
    
    def get_time(self) -> float:
        """
        Returns creation time

        :rtype: float
        :return: time
        """

        return self.creation
    
    def get_live(self) -> float:
        """
        Returns time of life

        :rtype: float
        :return: time
        """

        return self.time

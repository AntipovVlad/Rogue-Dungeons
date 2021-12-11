from .base_object import *


class Hero(BaseObject):
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

        super().__init__(en_y, en_x, 'hero', 'Ѫ')
        self.max_hp, self.hp = 3, 3
        self.armor = 1
        self.max_bombs, self.bombs = 3, 3
    
    def get_hp(self) -> int:
        """
        Returns hero's current health

        :rtype: int
        :return: hp
        """

        return self.hp
    
    def get_max_hp(self) -> int:
        """
        Returns hero's maximum health

        :rtype: int
        :return: hp
        """

        return self.max_hp
    
    def get_bombs(self) -> int:
        """
        Returns count of bombs

        :rtype: int
        :return: number of bombs
        """
        
        return self.bombs
    
    def is_dead(self) -> bool:
        """
        Checks whether hero alive or not

        :rtype: bool
        :return: is hero dead or not
        """
        
        return self.hp < 1
    
    def de_health(self, d: int = 1) -> None:
        """
        Decreases hero's health

        :param d: damage
        :type d: int
        """
        
        self.hp -= d
    
    def de_bombs(self) -> None:
        """
        Decreases hero's number of bombs

        :rtype: None
        :return: None
        """
        
        self.bombs -= 1
    
    def in_bombs(self) -> None:
        """
        Increases hero's number of bomns

        :rtype: None
        :return: None
        """
        
        self.bombs = min(self.bombs + 1, self.max_bombs)
    
    def set_possintion(self, en_y: int, en_x: int) -> None:
        """
        Changes hero's possition

        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int

        :rtype: None
        :return: None
        """
        
        self.y, self.x = en_y, en_x

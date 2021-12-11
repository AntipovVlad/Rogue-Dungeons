class BaseObject:
    """
    'Fish' for all game objects
    """
    
    def __init__(self, en_y: int, en_x: int, en_type: str, en_skin: str) -> None:
        """
        Initial function

        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int
        :param en_type: name of object
        :type en_type: str
        :param en_skin: skin of object
        :type en_skin: str

        :rtype: None
        :return: None
        """
        
        self.y, self.x = en_y, en_x
        self.type = en_type
        self.skin = en_skin
    
    def get_coordinates(self) -> tuple:
        """
        Returns coordinates of object

        :rtype: tuple
        :return: y coordinate, x coordinate
        """
        
        return (self.y, self.x)
    
    def get_skin(self) -> str:
        """
        Returns skin of object

        :rtype: str
        :return: skin
        """
        
        return self.skin

    def get_type(self) -> str:
        """
        Returns type of object

        :rtype: str
        :return: name of object
        """
        
        return self.type

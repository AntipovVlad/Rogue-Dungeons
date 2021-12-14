from random import choice, randint
from time import time


class Snake:
    """
    Class of snake enemy
    """
    
    def __init__(self, en_y: int, en_x: int, en_room: object, l: int = 0) -> None:
        """
        Initial function

        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int
        :param en_room: room where the object is placed
        :type en_room: object
        :param l: level
        :type l: int

        :rtype: None
        :return: None
        """

        self.hp = randint(3, 3 + l)
        self.body = [(en_y, en_x - i) for i in range(self.hp)]
        self.room = en_room
        self.direction = choice(['l', 't', 'r', 'b'])
        self.in_freeze = 1
        self.in_move = 0.2
        self.in_change = 1.6
        self.t_freeze = None
        self.t_move = time()
        self.t_change = time()
        self.type = 'enemy'
        self.skin = '◈'
    
    def get_type(self) -> str:
        """
        Returns name of object

        :rtype: str
        :return: name
        """
        
        return self.type
    
    def get_skin(self) -> str:
        """
        Returns snake's skin

        :rtype: str
        :return: skin
        """
        
        return self.skin
    
    def get_room(self) -> object:
        """
        Returns snake's room

        :rtype: object
        :return: room object
        """
        
        return self.room
    
    def get_health(self) -> int:
        """
        Returns snake's health

        :rtype: int
        :return: hp
        """
        
        return self.hp
    
    def is_freeze(self) -> bool:
        """
        Checks whether snake is freezed or not

        :rtype: bool
        :return: is snake freezed
        """
        
        return self.t_freeze is not None
    
    def can_extist(self, field: list, objects_coors: dict) -> bool:
        """
        Check whether snake can move here or not

        :param field: map array
        :type field: list
        :param object_coors: coordinates of new game object
        :type object_coors: dict

        :rtype: bool
        :return: fact of existence
        """
        
        flag = True
        for b in self.body:
            flag &= objects_coors.get(b) is None and field[b[0]][b[1]].get_type() == 'room' and field[b[0]][b[1]].get_skin() == ' '
        
        return flag
    
    def get_coordinates(self) -> list:
        """
        Returns coordinates of snake

        :rtype: None
        :return: snake coordinates
        """
        
        return self.body

    def de_freeze(self) -> None:
        """
        Releaves snake

        :rtype: None
        :return: None
        """
        
        if self.t_freeze is not None and float(time() - self.t_freeze) > self.in_freeze:
            self.t_freeze = None
    
    def set_freeze(self) -> None:
        """
        Stops snake for little time

        :rtype: None
        :return: None
        """
        
        self.t_freeze = time()
    
    def move(self, field: list, objects_coors: dict, hero: object) -> None:
        """
        Makes snake change possiotion

        :param field: map array
        :type field: list
        :param object_coors: coordinates of new game object
        :type object_coors: dict
        :param hero: Hero object
        :type hero: hero.Hero

        :rtype: None
        :return: None
        """
        
        if float(time() - self.t_move) > self.in_move:
            self.t_move = time()

            head = self.body[0]

            if self.direction == 'l':
                new_head = (head[0], head[1] - 1)
            elif self.direction == 'r':
                new_head = (head[0], head[1] + 1)
            elif self.direction == 't':
                new_head = (head[0] - 1, head[1])
            elif self.direction == 'b':
                new_head = (head[0] + 1, head[1])
            
            if field[new_head[0]][new_head[1]].get_type() == 'room':
                if objects_coors.get(new_head) is None and field[new_head[0]][new_head[1]].get_skin() == ' ':
                    objects_coors[new_head] = self
                    self.body.insert(0, new_head)
                    objects_coors.pop(self.body.pop())
                elif objects_coors.get(new_head) is not None and objects_coors.get(new_head).get_skin() == 'Ѫ':
                    hero.de_health()
                    self.t_freeze = time()
                    
                    self.change_direction(nes=True)
                else:
                    self.change_direction(nes=True)
            else:        
                self.change_direction(nes=True)

    def change_direction(self, nes: bool = False) -> None:
        """
        Makes snake change direction

        :param nes: obliged changing
        :type new: bool

        :rtype: None
        :return: None
        """
        
        if float(time() - self.t_change) > self.in_change or nes:
            self.t_change = time()
            if self.direction in ['l', 'r']:
                self.direction = choice(['t', 'b'])
            else:
                self.direction = choice(['l', 'r'])
    
    def de_health(self, objects_coors: dict, d: int = 1) -> bool:
        """
        Decreases snake health

        :param object_coors: coordinates of new game object
        :type object_coors: dict
        :param d: damage
        :type d: int

        :rtype: bool
        :return: whether snake was destroed or not
        """
        
        self.hp -= d
        objects_coors.pop(self.body.pop())

        return self.hp > 0

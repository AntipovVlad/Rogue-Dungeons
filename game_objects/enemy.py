from random import choice
from time import time


class Snake:
    def __init__(self, en_y: int, en_x: int, en_room: object) -> None:
        self.hp = 3
        self.body = [(en_y, en_x - i) for i in range(self.hp)]
        self.room = en_room
        self.direction = choice(['l', 't', 'r', 'b'])
        self.in_freeze = 2
        self.in_move = 0.2
        self.in_change = 1.6
        self.t_freeze = None
        self.t_move = time()
        self.t_change = time()
        self.type = 'enemy'
        self.skin = '#'
    
    def get_type(self) -> str:
        return self.type
    
    def get_skin(self) -> str:
        return self.skin
    
    def get_room(self) -> object:
        return self.room
    
    def can_extist(self, field: list, objects_coors: dict) -> bool:
        flag = True
        for b in self.body:
            flag &= objects_coors.get(b) is None and field[b[0]][b[1]].get_type() == 'room' and field[b[0]][b[1]].get_skin() == ' '
        
        return flag
    
    def get_coordinates(self):
        return self.body

    def de_freeze(self, tm) -> None:
        if self.t_freeze is not None and float(tm - self.t_freeze) > self.in_freeze:
            self.t_freeze = None
    
    def is_freeze(self) -> bool:
        return self.t_freeze is not None
    
    def move(self, field: list, objects_coors: dict, hero: object) -> None:
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
            
            if objects_coors.get(new_head) is None and field[new_head[0]][new_head[1]].get_type() == 'room':
                if field[new_head[0]][new_head[1]].get_skin() == ' ':
                    objects_coors[new_head] = self
                    self.body.insert(0, new_head)
                    objects_coors.pop(self.body.pop())
                elif field[new_head[0]][new_head[1]].get_skin() in ['@', 'a']:
                    hero.de_health()
                    self.t_freeze = time()
                else:
                    self.change_direction(nes=True)
            else:        
                self.change_direction(nes=True)

    def change_direction(self, nes=False) -> None:
        if float(time() - self.t_change) > self.in_change or nes:
            self.t_change = time()
            if self.direction in ['l', 'r']:
                self.direction = choice(['t', 'b'])
            else:
                self.direction = choice(['l', 'r'])
    
    def de_health(self, objects_coors, d=1) -> None:
        self.hp -= d
        objects_coors.pop(self.body.pop())

        if self.hp < 1:
            return self

from random import choice


class Snake:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.hp = 3
        self.body = [[en_y, en_x + 1], [en_y, en_x], [en_y, en_x - 1]]
        self.direction = choice(['l', 't', 'r', 'b'])
        self.freeze = 1
        self.t_freeze = None
        self.type = 'enemy'
    
    def get_type(self) -> str:
        return self.type
    
    def move(self, field: list):
        head = self.body[0]

        if self.direction == 'l':
            new_head = [head[0], head[1] - 1]
        elif self.direction == 'r':
            new_head = [head[0], head[1] + 1]
        elif self.direction == 't':
            new_head = [head[0] - 1, head[1]]
        elif self.direction == 'b':
            new_head = [head[0] + 1, head[1]]
        
        if field[new_head[0]][new_head[1]].get_type() == 'room' and field[new_head[0]][new_head[1]].get_skin() in [' ', '@', 'a']:
            self.body.insert(0, new_head)
        
            e_body = self.body.pop()

            return new_head, e_body
    
    def change_direction(self) -> None:
        if self.direction in ['l', 'r']:
            self.direction = choice(['t', 'b'])
        else:
            self.direction = choice(['l', 'r'])
    
    def de_health(self, d=1) -> None:
        self.hp -= d
        self.body.pop()

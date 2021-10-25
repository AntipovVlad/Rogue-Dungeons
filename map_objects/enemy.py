class Enemy:
    def __init__(self, en_y: int, en_x: int) -> None:
        self.hp = 3
        self.body = [[en_y, en_x + 1], [en_y, en_x], [en_y, en_x - 1]]

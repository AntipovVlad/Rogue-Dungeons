class Block:
    def __init__(self, en_y: int, en_x: int, en_type: str) -> None:
        self.locked = False
        self.number = 2 ** 16
        self.zone = None
        self.block_type = en_type
        self.skin = ''
        self.visibility = False

        self.y = en_y
        self.x = en_x
    
    def lock_block(self) -> None:
        self.locked = True
    
    def set_number(self, en_number: int) -> None:
        self.number = en_number
    
    def make_visible(self) -> None:
        self.visibility = True
    
    def null(self) -> None:
        self.number = 2 ** 16
    
    def is_locked(self) -> bool:
        return self.locked
    
    def is_counted(self) -> bool:
        return self.number != 2 ** 16
    
    def is_visible(self) -> bool:
        return self.visibility
    
    def get_number(self) -> int:
        return self.number
    
    def get_zone(self) -> object:
        return self.zone
    
    def get_type(self) -> str:
        return self.block_type
    
    def get_skin(self) -> str:
        return self.skin


class Zone:
    def __init__(self) -> None:
        self.opened = False
    
    def open(self):
        for obj in self.blocks:
            obj.make_visible()
    
    def add_block(self, block: object) -> None:
        self.blocks.append(block)


class StoneBlock(Block):
    def __init__(self, en_y: int, en_x: int, r: int) -> None:
        super().__init__(en_y, en_x, 'stone')
        self.skin = '█' if r % 25 == 0 else ' '
        
        self.make_visible()


class RoomBlock(Block):
    def __init__(self, en_y: int, en_x: int, en_zone: object, en_wall: str) -> None:
        super().__init__(en_y, en_x, 'room')

        self.zone = en_zone
        self.skin = {'': ' ', 'l': '║', 'r': '║', 't': '═', 'b': '═', 'lt': '╔', 'rt': '╗', 'lb': '╚', 'rb': '╝'}[en_wall]

        self.lock_block()


class BridgeBlock(Block):
    def __init__(self, en_y: int, en_x: int, en_zone: object) -> None:
        super().__init__(en_y, en_x, 'bridge')
        
        self.skin = ' '
        self.zone = en_zone
        self.activator, self.rb = False, None

        self.lock_block()
    
    def get_room(self) -> object:
        return self.rb
    
    def set_activator(self, sur: list) -> None:
        for s in sur:
            if s.get_type() == 'room' and not s.is_visible():
                self.activator = True
                self.rb = s
                break
    
    def activate(self) -> bool:
        if self.activator:
            self.activator = False
            self.rb.get_zone().open()

            return True
        
        return False


class Room(Zone):
    def __init__(self, coors: list) -> None:
        self.lt_y, self.lt_x = coors[0]
        self.rb_y, self.rb_x = coors[1]
        self.activated = False
        self.cleared = False

        self.blocks = []
        self.bridges = []
        self.enemies = []
    
    def get_coordinates(self) -> tuple:
        return self.lt_y, self.lt_x, self.rb_y, self.rb_x
    
    def get_enemies(self) -> list:
        return self.enemies
    
    def is_cleared(self) -> bool:
        return self.cleared
    
    def del_enemy(self, en) -> None:
        self.enemies.remove(en)
    
    def clear(self) -> None:
        self.cleared = True

    def open_bridges(self) -> None:
        for bridge in self.bridges:
            bridge.open()

            yield bridge.get_conn_dots(), bridge

    
    def add_bridge(self, bridge: object):
        self.bridges.append(bridge)
    
    def is_activated(self) -> bool:
        return self.activated
    
    def activate(self, en_enemies: list = []) -> None:
        if not self.activated:
            self.activated = True
            self.enemies = en_enemies.copy()


class Bridge(Zone):
    def __init__(self) -> None:
        super().__init__()

        self.rooms = []
        self.blocks = []
        self.conn_dots = []
    
    def get_conn_dots(self) -> list:
        return self.conn_dots
    
    def add_room(self, room: object, en_y: int, en_x: int):
        self.rooms.append(room)
        self.conn_dots.append((en_y, en_x))

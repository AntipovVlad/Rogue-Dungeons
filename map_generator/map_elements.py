from random import choice, randint


class Block:
    """
    Base class for elements of map
    """

    def __init__(self, en_y: int, en_x: int, en_type: str) -> None:
        """
        Initial function

        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int
        :param en_type: name of block
        :type en_type: str

        :rtype: None
        :return: None
        """
        
        self.locked = False
        self.number = 2 ** 16
        self.zone = None
        self.block_type = en_type
        self.skin = ''
        self.visibility = False

        self.y = en_y
        self.x = en_x
    
    def lock_block(self) -> None:
        """
        Sets True for param 'locked'

        :rtype: None
        :return: None
        """

        self.locked = True
    
    def set_number(self, en_number: int) -> None:
        """
        Sets coordinate of block in island search 

        :param en_number: coordinate
        :type en_number: int

        :rtype: None
        :return: None
        """

        self.number = en_number
    
    def make_visible(self) -> None:
        """
        Sets True for param 'visibility'

        :rtype: None
        :return: None
        """

        self.visibility = True
    
    def null(self) -> None:
        """
        Nullify param 'number'

        :rtype: None
        :return: None
        """
        
        self.number = 2 ** 16
    
    def is_locked(self) -> bool:
        """
        Whether block can be changed or not

        :rtype: bool
        :return: param 'locked'
        """
        
        return self.locked
    
    def is_counted(self) -> bool:
        """
        Whether block is used for island search or not

        :rtype: bool
        :return: number of block
        """

        return self.number != 2 ** 16
    
    def is_visible(self) -> bool:
        """
        Whether block can be drawn on screen or not

        :rtype: bool
        :return: param 'visibility'
        """

        return self.visibility
    
    def get_number(self) -> int:
        """
        Returns number of block in island search

        :rtype: int
        :return: param 'number'
        """

        return self.number
    
    def get_zone(self) -> object:
        """
        Returns room where block is placed

        :rtype: object
        :return: param 'zone'
        """

        return self.zone
    
    def get_type(self) -> str:
        """
        Returns name of block

        :rtype: str
        :return: param 'block_type'
        """

        return self.block_type
    
    def get_skin(self) -> str:
        """
        Returns skin of block

        :rtype: str
        :return: param 'skin'
        """

        return self.skin


class Zone:
    """
    Base class for object of map
    """

    def __init__(self) -> None:
        """
        Initial function

        :rtype: None
        :return: None
        """
        
        self.opened = False
    
    def open(self):
        """
        Makes all blocks of object visible on screen and active

        :rtype: None
        :return: None
        """
        
        for obj in self.blocks:
            obj.make_visible()
    
    def add_block(self, block: object) -> None:
        """
        Addes new block in object

        :param block: block objects
        :type block: object

        :rtype: None
        :return: None
        """
        
        self.blocks.append(block)


class StoneBlock(Block):
    """
    Class of stone block
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
        
        super().__init__(en_y, en_x, 'stone')
        self.skin = choice(['✦', '✧', '◈']) if randint(0, 100) % 25 == 0 else ' '
        self.make_visible()


class RoomBlock(Block):
    """
    Class of room block
    """
    
    def __init__(self, en_y: int, en_x: int, en_zone: object, en_wall: str) -> None:
        """
        Initial function

        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int
        :param en_zone: room object where block is placed
        :type en_zone: object
        :param en_wall: type of wall
        :type en_wall: str

        
        :rtype: None
        :return: None
        """

        super().__init__(en_y, en_x, 'room')

        self.zone = en_zone
        self.skin = {'': ' ', 'l': '▌', 'r': '▐', 't': '▀', 'b': '▄', 'lt': '▛', 'rt': '▜', 'lb': '▙', 'rb': '▟'}[en_wall]
        self.wall = en_wall
        self.lock_block()
    
    def get_wall(self) -> str:
        """
        Returns type of wall

        :rtype: str
        :return: param 'wall'
        """
        
        return self.wall


class BridgeBlock(Block):
    """
    Class of bridge block
    """
    
    def __init__(self, en_y: int, en_x: int, en_zone: object) -> None:
        """
        Initial function

        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int
        :param en_zone: room object where block is placed
        :type en_zone: object
        
        :rtype: None
        :return: None
        """

        super().__init__(en_y, en_x, 'bridge')
        
        self.skin = ' '
        self.zone = en_zone
        self.activator, self.rb = False, None

        self.lock_block()
    
    def get_room(self) -> object:
        """
        Returns room object that is activated by this block

        :rtype: object
        :return: param 'rb'
        """

        return self.rb
    
    def is_activator(self) -> bool:
        """
        Whether block activates room or not

        :rtype: bool
        :return: param 'activator'
        """
        
        return self.activator
    
    def set_activator(self, sur: list) -> bool:
        """
        Makes block an activator

        :param sur: surrounding
        :param type: list

        :rtype: bool
        :return: whether block made or not
        """
        
        for s in sur:
            if s.get_type() == 'room' and not s.is_visible():
                self.activator = True
                self.rb = s.get_zone()
                
                return True
        
        return False
    
    def activate(self) -> bool:
        """
        Activates room

        :rtype: bool
        :return: whether room activated or not
        """
        
        if self.activator:
            self.activator = False
            self.rb.open()

            return True
        
        return False


class Room(Zone):
    """
    Class of room zone
    """
    
    def __init__(self, coors: list) -> None:
        """
        Initial function

        :param coors: array of coordinates
        :param type: list

        :rtype: None
        :return: None
        """
        
        self.lt_y, self.lt_x = coors[0]
        self.rb_y, self.rb_x = coors[1]
        self.activated = False
        self.cleared = False

        self.blocks = []
        self.bridges = []
        self.enemies = set()
    
    def get_coordinates(self) -> tuple:
        """
        Returns coordinates of room

        :rtype: tuple
        :return: params 'lt_y', 'lt_x', 'rb_y', 'rb_x'
        """
        
        return self.lt_y, self.lt_x, self.rb_y, self.rb_x
    
    def get_enemies(self) -> set:
        """
        Returns list of enemies

        :rtype: set
        :return: param 'enemies'
        """
        
        return self.enemies
    
    def is_cleared(self) -> bool:
        """
        Whether all enemies destroyed or not

        :rtype: bool
        :return: param 'cleared'
        """
        
        return self.cleared
    
    def del_enemy(self, en) -> None:
        """
        Deletes enemy from list

        :rtype: None
        :return: None
        """
        
        self.enemies.discard(en)
    
    def clear(self) -> None:
        """
        Sets True for param 'cleared'

        :rtype: None
        :return: None
        """
        
        self.cleared = True

    def open_bridges(self) -> tuple:
        """
        Makes all bridges adjoined to this room visible

        :rtype: tuple
        :return: coordinates of bridge blocks that activates room and bridge object
        """
        
        for bridge in self.bridges:
            bridge.open()

            yield bridge.get_conn_dots(), bridge

    def add_bridge(self, bridge: object) -> None:
        """
        Addes bridge object in list

        :rtype: None
        :return: None
        """
        
        self.bridges.append(bridge)
    
    def is_activated(self) -> bool:
        """
        Whether room is activated or not

        :rtype: bool
        :return: param 'activated'
        """
        
        return self.activated
    
    def activate(self, en_enemies: list = []) -> None:
        """
        Activates room

        :param en_enemies: list of enemies in room
        :type en_enemies: list

        :rtype: None
        :return: None
        """
        
        if not self.activated:
            self.activated = True
            self.enemies = set(en_enemies.copy())


class Bridge(Zone):
    """
    Class of bridge zone
    """
    
    def __init__(self) -> None:
        """
        Initial function

        :rtype: None
        :return: None
        """
        
        super().__init__()

        self.rooms = []
        self.blocks = []
        self.conn_dots = []
    
    def get_conn_dots(self) -> list:
        """
        Returns list of blocks that connect bridge and rooms

        :rtype: list
        :return: param 'conn_dots'
        """
        
        return self.conn_dots
    
    def add_room(self, room: object, en_y: int, en_x: int) -> None:
        """
        Addes room object in list and coordinates of blocks that connects bridge and room

        :param room: room object
        :type room: object
        :param en_y: y coordinate
        :type en_y: int
        :param en_x: x coordinate
        :type en_x: int

        :rtype: None
        :return: None
        """
        
        self.rooms.append(room)
        self.conn_dots.append((en_y, en_x))

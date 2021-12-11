import enum
from shutil import get_terminal_size
from .map_elements import *
from random import randint, choice
from time import sleep

class Screen(enum.Enum):
    """
    Constants for game screen
    """

    s_width, s_height = get_terminal_size()
    b_height, f_height = int(0.1 * s_height), int(0.8 * s_height)


def is_free(field: list, lt_y: int, lt_x: int, height: int, width: int) -> bool:
    """
    Checking if room can be created in chosen coorinates
 
    :param field: map field array
    :type field: list
    :param lt_y: left-top y coordinate
    :type lt_y: int
    :param lt_x: left-top x coordinate
    :type lt_x: int
    :param height: height of room
    :type height: int
    :param width: width of room
    :type width: int
    
    :rtype: bool
    :return: is it possible to create room
    """

    flag = True

    for i in range(height):
        for j in range(width):
            flag = flag and not field[lt_y + i][lt_x + j].is_locked()
    
    return flag

def create_room(field: list, free_blocks: list, rooms: list) -> bool:
    """
    Creating room
 
    :param field: map field array
    :type field: list
    :param free_blocks: array of free blocks
    :type free_blocks: list
    :param rooms: array of created rooms
    :type rooms: list
    
    :rtype: bool
    :return: whether created room or not
    """

    # ========= Counting size of room ========
    n_min = 10
    n_max = 0.5

    a = randint(n_min, int(n_max * Screen.f_height.value))
    b = randint(n_min, int(n_max * Screen.s_width.value))

    # ========= Searching place for room ========
    y, x = choice(free_blocks)

    while y + a - 1 >= Screen.f_height.value - 1 or x + b - 1 >= Screen.s_width.value - 1 or not is_free(field, y, x, a, b):
        free_blocks.remove((y, x))
        if len(free_blocks) == 0:
            return False

        y, x = choice(free_blocks)
    
    # ========= Creating room and matching it on map ========
    room = Room([(y, x), (y + a - 1, x + b - 1)])
    for i in range(y, y + a):
        for j in range(x, x + b):
            wall = ''
            
            if x + b - 1 - j == 0:
                wall += 'r'
            if j - x == 0:
                wall += 'l'
            if y + a - 1 - i == 0:
                wall += 'b'
            if i - y == 0:
                wall += 't'
            
            r_block = RoomBlock(i, j, room, wall)
            field[i][j] = r_block
            room.add_block(r_block)
        
    rooms.append(room)

    for i in range(max(0, y - 4), min(y + a + 4, Screen.f_height.value)):
        for j in range(max(0, x - 8), min(x + b + 8, Screen.s_width.value)):
            if field[i][j].__class__.__name__ == 'StoneBlock':
                field[i][j].lock_block()

    return True


def find_room(field: list, room: Room) -> tuple:
    """
    Searching the closest room for last created room
 
    :param field: map field array
    :type field: list
    :param room: recently created room
    :type room: Room
    
    :rtype: tuple
    :return: coordinates of founded room and distance between rooms
    """

    lt_y, lt_x, rb_y, rb_x = room.get_coordinates()
    d_numbers = {0: []}
    step = 0

    for i in range(lt_y, rb_y + 1):
        for j in range(lt_x, rb_x + 1):
            case = int(i - lt_y == 0) + int(j - lt_x == 0) + int(i - rb_y == 0) + int(j - rb_x == 0)

            if case == 1:
                field[i][j].set_number(step)
                d_numbers[step].append((i, j))
    
    while True:
        for s in d_numbers[step]:
            for coor in [[s[0] - 1, s[1]], [s[0] + 1, s[1]], [s[0], s[1] - 1], [s[0], s[1] + 1]]:
                if coor[0] < 1:
                    coor[0] = 1
                if coor[0] > Screen.f_height.value - 2:
                    coor[0] = Screen.f_height.value - 2
                if coor[1] < 1:
                    coor[1] = 1
                if coor[1] > Screen.s_width.value - 2:
                    coor[1] = Screen.s_width.value - 2
                
                if field[coor[0]][coor[1]].get_zone() is room or field[coor[0]][coor[1]].get_type() == 'room' and field[coor[0]][coor[1]].get_wall() in ['lt', 'rt', 'lb', 'rb']:
                    continue
                
                n = False
                for n_coor in [[coor[0] - 1, coor[1]], [coor[0] + 1, coor[1]], [coor[0], coor[1] - 1], [coor[0], coor[1] + 1], [coor[0] - 1, coor[1] - 1], [coor[0] + 1, coor[1] + 1], [coor[0] + 1, coor[1] - 1], [coor[0] - 1, coor[1] + 1]]:
                    if field[n_coor[0]][n_coor[1]].get_type() == 'room' and field[n_coor[0]][n_coor[1]].get_wall() in ['lt', 'rt', 'lb', 'rb']:
                        n = True
                        break
                
                if n:
                    continue

                if not field[coor[0]][coor[1]].is_counted():
                    if field[coor[0]][coor[1]].get_type() == 'bridge' or field[coor[0]][coor[1]].get_type() == 'room':
                        return coor[0], coor[1], step + 1
                    
                    field[coor[0]][coor[1]].set_number(step + 1)
                    if d_numbers.get(step + 1) is None:
                        d_numbers[step + 1] = [coor]
                    else:
                        d_numbers[step + 1].append(coor)
        
        step += 1


def create_bridge(field: list, room: Room, bridges: list) -> None:
    """
    Creating bridge between current and the nearest rooms
 
    :param field: map field array
    :type field: list
    :param room: current room
    :type room: Room
    :param bridges: array of bridges
    :type bridges: list
    
    :rtype: None
    :return: None
    """
    
    y, x, s = find_room(field, room)

    if field[y][x].get_type() == 'bridge':
        bridge = field[y][x].get_zone()
    else:
        bridge = Bridge()
        bridge.add_room(field[y][x].get_zone(), y, x)
        field[y][x].get_zone().add_bridge(bridge)

        bridges.append(bridge)

    while s != 1:
        if field[y - 1][x].get_number() == s - 1:
            y = max(1, y - 1)
        elif field[y + 1][x].get_number() == s - 1:
            y = min(Screen.f_height.value - 2, y + 1)
        elif field[y][x - 1].get_number() == s - 1:
            x = max(1, x - 1)
        elif field[y][x + 1].get_number() == s - 1:
            x = min(Screen.s_width.value - 2, x + 1)
        
        field[y][x] = BridgeBlock(y, x, bridge)
        bridge.add_block(field[y][x])
        for i in range(max(0, y - 2), min(y + 2, Screen.f_height.value)):
            for j in range(max(0, x - 2), min(x + 2, Screen.s_width.value)):
                if field[i][j].get_type() == 'stone':
                    field[i][j].lock_block()
        
        s -= 1
    
    if field[y - 1][x].get_number() == s - 1:
        y = max(1, y - 1)
    elif field[y + 1][x].get_number() == s - 1:
        y = min(Screen.f_height.value - 2, y + 1)
    elif field[y][x - 1].get_number() == s - 1:
        x = max(1, x - 1)
    elif field[y][x + 1].get_number() == s - 1:
        x = min(Screen.s_width.value - 2, x + 1)
    
    bridge.add_room(room, y, x)
    room.add_bridge(bridge)

    for i in range(Screen.f_height.value):
        for j in range(Screen.s_width.value):
            field[i][j].null()


def generate_map(rooms_number: int) -> tuple:
    """
    Creates map of level
 
    :param rooms_number: number of rooms for map
    :type rooms_number: int
    
    :rtype: tuple
    :return: map, array of rooms, array of bridjes
    """

    field = [[StoneBlock(i, j) for j in range(Screen.s_width.value)] for i in range(Screen.f_height.value)]
    rooms, bridges = [], []
    free_blocks = []
    for i in range(1, Screen.f_height.value - 1):
        for j in range(1, Screen.s_width.value - 1):
            free_blocks.append((i, j))
    
    create_room(field, free_blocks, rooms)
    for _ in range(rooms_number - 1):
        b = create_room(field, free_blocks, rooms)
        if not b:
            break
        create_bridge(field, rooms[-1], bridges)
        
    return field, rooms, bridges

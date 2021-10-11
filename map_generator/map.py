import enum
from shutil import get_terminal_size
from map_elements import *
from random import randint, choice
from colorama import Back, Style


class Screen(enum.Enum):
    """
    Constants for game screen
    """

    s_width, s_height = get_terminal_size()
    b_height, f_height = int(0.1 * s_height), int(0.8 * s_height)


def is_free(field: list, lt_y: int, lt_x: int, height: int, width: int):
    """
    Checking if island can be created in chosen coorinates
    """

    flag = True

    for i in range(height):
        for j in range(width):
            flag = flag and not field[lt_y + i][lt_x + j].is_locked()
    
    return flag

def create_island(field: list, free_blocks: list, islands: list, islands_number) -> bool:
    """
    Creating island
    """

    # ========= Counting size of island ========
    n_min = 5
    n_max = 0.2

    a = randint(n_min, int(n_max * Screen.f_height.value))
    b = randint(n_min, int(n_max * Screen.s_width.value))

    # ========= Searching place for island ========
    y, x = choice(free_blocks)

    while y + a - 1 >= Screen.f_height.value - 1 or x + b - 1 >= Screen.s_width.value - 1 or not is_free(field, y, x, a, b):
        free_blocks.remove((y, x))
        if len(free_blocks) == 0:
            return False

        y, x = choice(free_blocks)
    
    # ========= Creating island and matching it on map ========
    island = RectangularIsland([(y, x), (y + a - 1, x + b - 1)])
    for i in range(y, y + a):
        for j in range(x, x + b):
            beach = (i - y) * (j - x) * (y + a - 1 - i) * (x + b - 1 - j) == 0
            field[i][j] = GroundBlock(i, j, island, beach)
        
    islands.append(island)

    for i in range(max(0, y - 4), min(y + a + 4, Screen.f_height.value)):
        for j in range(max(0, x - 8), min(x + b + 8, Screen.s_width.value)):
            if field[i][j].__class__.__name__ == 'SeaBlock':
                field[i][j].lock_block()

    return True

def find_island(field, island) -> tuple:
    """
    Searching the closest island for last created island
    """

    lt_y, lt_x, rb_y, rb_x = island.get_coordinates()
    d_numbers = {0: []}
    step = 0

    for i in range(lt_y, rb_y + 1):
        for j in range(lt_x, rb_x + 1):
            case = int(i - lt_y == 0) + int(j - lt_x == 0) + int(i - rb_y == 0) + int(j - rb_x == 0)

            if case > 0:
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
                
                if field[coor[0]][coor[1]].get_island() is island:
                    continue

                if not field[coor[0]][coor[1]].is_counted():
                    if field[coor[0]][coor[1]].__class__.__name__ == 'BridgeBlock' or field[coor[0]][coor[1]].__class__.__name__ == 'GroundBlock' and field[coor[0]][coor[1]].get_island() is not island:
                        return coor[0], coor[1], step + 1
                    
                    field[coor[0]][coor[1]].set_number(step + 1)
                    if d_numbers.get(step + 1) is None:
                        d_numbers[step + 1] = [coor]
                    else:
                        d_numbers[step + 1].append(coor)
        
        step += 1


def create_bridge(field, island) -> None:
    """
    Creating bridge between current and the nearest islands
    """
    
    y, x, s = find_island(field, island)

    while s != 1:
        if field[y - 1][x].get_number() == s - 1:
            y = max(1, y - 1)
        elif field[y + 1][x].get_number() == s - 1:
            y = min(Screen.f_height.value - 2, y + 1)
        elif field[y][x - 1].get_number() == s - 1:
            x = max(1, x - 1)
        elif field[y][x + 1].get_number() == s - 1:
            x = min(Screen.s_width.value - 2, x + 1)
        
        field[y][x] = BridgeBlock(y, x)
        for i in range(max(0, y - 2), min(y + 2, Screen.f_height.value)):
            for j in range(max(0, x - 2), min(x + 2, Screen.s_width.value)):
                if field[i][j].__class__.__name__ == 'SeaBlock':
                    field[i][j].lock_block()
        
        s -= 1
    
    for i in range(Screen.f_height.value):
        for j in range(Screen.s_width.value):
            field[i][j].null()
    

def generate_map(islands_number: int) -> list:
    """
    Generating map for current level
    """

    field = [[SeaBlock(i, j) for j in range(Screen.s_width.value)] for i in range(Screen.f_height.value)]
    islands = []
    free_blocks = []
    for i in range(1, Screen.f_height.value - 1):
        for j in range(1, Screen.s_width.value - 1):
            free_blocks.append((i, j))
    
    create_island(field, free_blocks, islands, islands_number)
    for _ in range(islands_number - 1):
        b = create_island(field, free_blocks, islands, islands_number)
        if not b:
            break
        create_bridge(field, islands[-1])
    
    return field

FIELD = generate_map(10)
for _ in range(Screen.b_height.value):
    print('=')
for f in FIELD:
    for ff in f:
        if ff.__class__.__name__ == 'SeaBlock':
            print(f'{Back.BLUE} {Style.RESET_ALL}', end='')
        elif ff.__class__.__name__ == 'GroundBlock':
            print(f'{Back.GREEN} {Style.RESET_ALL}', end='')
        elif ff.__class__.__name__ == 'BridgeBlock':
            print(f'{Back.BLACK} {Style.RESET_ALL}', end='')
for _ in range(Screen.b_height.value):
    print('=')
# ║ ═ ╔ ╗ ╚ ╝

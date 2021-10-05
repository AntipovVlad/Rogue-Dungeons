import enum
from shutil import get_terminal_size
from map_elements import *
from random import randint, choice


class Screen(enum.Enum):
    s_width, s_height = get_terminal_size()
    b_height, f_height = int(0.1 * s_height), int(0.8 * s_height)


def is_free(field: list, lt_y: int, lt_x: int, height: int, width: int):
    flag = True

    for i in range(height):
        for j in range(width):
            flag &= field[lt_y + i][lt_x + j].is_locked()

            if not flag:
                return flag
    
    return flag

def create_island(field: list, free_blocks: list, islands: list, islands_number) -> bool:
    n_min = [20, 18, 16, 14, 12, 10][islands_number]
    n_max = [0.45, 0.3, 0.25, 0.2, 0.18, 0.15][islands_number]

    a = randint(n_min, int(n_max * Screen.f_height.value))
    b = randint(int(n_min * 1.5), int(n_max * Screen.s_width.value))
    y, x = choice(free_blocks)

    while y + a - 1 >= Screen.f_height.value or x + b - 1 >= Screen.s_width.value or not is_free(field, y, x, a, b):
        free_blocks.remove((y, x))
        if len(free_blocks) == 0:
            return False

        y, x = choice(free_blocks)
    
    island = RectangularIsland([(y, x), (y + a - 1, x + b - 1)])
    for i in range(y, y + a):
        for j in range(x, x + b):
            field[i][j] = GroundBlock(i, j, island)
    
    islands.append(island)

    return True


def create_bridge(field) -> None:
    pass

def generate_map(islands_number: int) -> list:
    field = [[SeaBlock() for __ in range(Screen.s_width.value)] for _ in range(Screen.f_height.value)]
    islands = []
    free_blocks = [[(y, x) for y in range(1, Screen.s_width.value - 1)] for x in range(1, Screen.f_height.value - 1)]
    
    for _ in range(islands_number):
        create_island(field, free_blocks, islands, islands_number)
        create_bridge(field)
    
    return field

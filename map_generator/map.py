import enum
from shutil import get_terminal_size
from map_elements import *
from random import randint, choice


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
            flag &= field[lt_y + i][lt_x + j].is_locked()

            if not flag:
                return flag
    
    return flag

def create_island(field: list, free_blocks: list, islands: list, islands_number) -> bool:
    """
    Creating island
    """

    # ========= Counting size of island ========
    n_min = [20, 18, 16, 14, 12, 10][islands_number]
    n_max = [0.45, 0.3, 0.25, 0.2, 0.18, 0.15][islands_number]

    a = randint(n_min, int(n_max * Screen.f_height.value))
    b = randint(int(n_min * 1.5), int(n_max * Screen.s_width.value))

    # ========= Searching place for island ========
    y, x = choice(free_blocks)

    while y + a - 1 >= Screen.f_height.value or x + b - 1 >= Screen.s_width.value or not is_free(field, y, x, a, b):
        free_blocks.remove((y, x))
        if len(free_blocks) == 0:
            return False

        y, x = choice(free_blocks)
    
    # ========= Creating island and matching it on map ========
    island = RectangularIsland([(y, x), (y + a - 1, x + b - 1)])
    for i in range(y, y + a):
        for j in range(x, x + b):
            b = (i - y) * (j - x) * (y + a - 1 - i) * (x + b - 1 - j) == 0
            field[i][j] = GroundBlock(i, j, island, b)
    
    islands.append(island)

    return True



def create_bridge(field, island) -> None:
    """
    Creating bridge between current and the nearest islands
    """
    def find_island() -> tuple:
        lt_y, lt_x, rb_y, rb_x = island.get_coordinates()
        step = 0

        while True:
            step += 1
            lt_y, lt_x = max(1, lt_y - 1), max(1, lt_x - 1)
            rb_y, rb_x = min(Screen.f_height.value - 2, rb_y + 1), min(Screen.s_width.value - 2, rb_x + 1)

            for i in range(lt_y, rb_y + 1):
                for j in range(lt_x, rb_x + 1):
                    if field[i][j].__class__.__name__ == 'GroundBlock' and field[i][j].get_island() is not island:
                        return i, j, step
                    
                    case = int(i - lt_y == 0) + int(j - lt_x == 0) + int(i - rb_y == 0) + int(j - rb_x == 0)
                    if case == 1 and not (field[i][j].is_locked() or field[i][j].is_counted()):
                        field[i][j].count(step)
                    elif case == 2 and not (field[i][j].is_locked() or field[i][j].is_counted()):
                        field[i][j].count(step + 1)
    
    y, x, step = find_island()
    while step != 1:
        if field[y - 1][x].get_number() == step - 1:
            y -= 1
        elif field[y + 1][x].get_number() == step - 1:
            y += 1
        elif field[y][x - 1].get_number() == step - 1:
            x -= 1
        elif field[y][x + 1].get_number() == step - 1:
            x += 1
        
        field[y][x] = BridgeBlock(y, x)
        step -= 1
    

def generate_map(islands_number: int) -> list:
    """
    Generating map for current level
    """

    field = [[SeaBlock() for __ in range(Screen.s_width.value)] for _ in range(Screen.f_height.value)]
    islands = []
    free_blocks = [[(y, x) for y in range(1, Screen.s_width.value - 1)] for x in range(1, Screen.f_height.value - 1)]
    
    create_island(field, free_blocks, islands, islands_number)
    for _ in range(islands_number - 1):
        create_island(field, free_blocks, islands, islands_number)
        create_bridge(field, islands[-1])
    
    return field

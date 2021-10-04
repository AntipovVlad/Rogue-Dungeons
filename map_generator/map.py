import enum
from shutil import get_terminal_size
from map_elements import *

class Screen(enum.Enum):
    s_width, s_height = get_terminal_size()
    b_height, f_height = int(0.1 * s_height), int(0.8 * s_height)


def create_island():
    pass

def create_bridge():
    pass

def generate_map(islands_number: int) -> list:
    field = [[SeaBlock() for __ in range(Screen.s_width.value)] for _ in range(Screen.f_height.value)]
    
    for _ in range(islands_number):
        create_island()
        create_bridge()
    
    return field

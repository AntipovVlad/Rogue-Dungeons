import curses
from os import SEEK_DATA
import time
from map_generator import map, map_elements
from game_objects import hero, enemy, bomb
from curses import textpad

menu = ['Play', 'Scoreboard', 'Exit']
objects = {'Hero': None, 'Enemies': [], 'Bombs': []}

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()


def add_str(stdscr, y, x, s, t) -> None:
    stdscr.attron(curses.color_pair(t))
    stdscr.addstr(y, x, s)
    stdscr.attroff(curses.color_pair(t))


def play(stdscr):
    global objects

    levels = 1

    for _ in range(levels):
        field, rooms, bridges = map.generate_map(5)
        h, w = stdscr.getmaxyx()
        y, x = int(h * 0.1), 0

        cur_room = rooms[0]
        cur_room.open()
        cur_room.activate()

        lt_y, lt_x, rb_y, rb_x = cur_room.get_coordinates()
        hy, hx = (lt_y + rb_y) // 2, (lt_x + rb_x) // 2

        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j].get_type() == 'stone':
                    t = 2
                elif field[i][j].get_type() == 'room':
                    t = 4 if field[i][j].is_visible() else 2
                elif field[i][j].get_type() == 'bridge':
                    t = 4 if field[i][j].is_visible() else 2
                
                add_str(stdscr, y + i, x + j, field[i][j].get_skin(), t)

                stdscr.refresh()

        objects['Hero'] = hero.Hero(hy, hx)

        while 1:
            for obj in objects:
                if obj == 'Hero':
                    t = 4
                    add_str(stdscr, y + hy, hx, '@', t)
            
            key = stdscr.getch()

            if key == ord('w') and field[hy - 1][hx].get_skin() == ' ':
                t = 4 if field[hy][hx].get_type() == 'room' else 1
                add_str(stdscr, y + hy, hx, field[hy][hx].get_skin(), t)

                hy -= 1
            elif key == ord('s') and field[hy + 1][hx].get_skin() == ' ':
                t = 4 if field[hy][hx].get_type() == 'room' else 1
                add_str(stdscr, y + hy, hx, field[hy][hx].get_skin(), t)

                hy += 1
            elif key == ord('a') and field[hy][hx - 1].get_skin() == ' ':
                t = 4 if field[hy][hx].get_type() == 'room' else 1
                add_str(stdscr, y + hy, hx, field[hy][hx].get_skin(), t)

                hx -= 1
            elif key == ord('d') and field[hy][hx + 1].get_skin() == ' ':
                t = 4 if field[hy][hx].get_type() == 'room' else 1
                add_str(stdscr, y + hy, hx, field[hy][hx].get_skin(), t)
                
                hx += 1
            elif key == ord('o'):
                if field[hy][hx].get_type() == 'room':
                    cur_room = field[hy][hx].get_zone()
                
                for dots, bridge in cur_room.open_bridges():
                    for dot in dots:
                        field[dot[0]][dot[1]] = map_elements.BridgeBlock(dot[0], dot[1], bridge)
                        field[dot[0]][dot[1]].set_activator([field[dot[0] - 1][dot[1]], field[dot[0] + 1][dot[1]], field[dot[0]][dot[1] - 1], field[dot[0]][dot[1] + 1]])
                            
                for i in range(len(field)):
                    for j in range(len(field[0])):
                        if field[i][j].get_type() == 'bridge':
                            t = 1 if field[i][j].is_visible() else 2
                        
                            add_str(stdscr, y + i, x + j, field[i][j].get_skin(), t)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break
            
            if field[hy][hx].get_type() == 'bridge':
                field[hy][hx].activate()

                for i in range(len(field)):
                    for j in range(len(field[0])):
                        if field[i][j].get_type() == 'room':
                            t = 4 if field[i][j].is_visible() else 2
        
                            add_str(stdscr, y + i, x + j, field[i][j].get_skin(), t)
            
            stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    current_row_idx = 0
    
    print_menu(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu):
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu[current_row_idx] == 'Exit':
                break
            
            if menu[current_row_idx] == 'Play':
                play(stdscr)

            stdscr.clear()
            stdscr.addstr(0, 0, f'You pressed {menu[current_row_idx]}')
            stdscr.refresh()
            stdscr.getch()
        
        print_menu(stdscr, current_row_idx)
        stdscr.refresh()


try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass

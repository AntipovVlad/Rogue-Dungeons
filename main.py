import curses
from os import SEEK_DATA
import time
from map_generator import map
from map_objects import hero, enemy, bomb
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


def del_foot(stdscr, y, x, t) -> None:
    stdscr.attron(curses.color_pair(t))
    stdscr.addstr(y, x, ' ')
    stdscr.attroff(curses.color_pair(t))


def play(stdscr):
    global objects

    levels = 1

    for _ in range(levels):
        field, islands = map.generate_map(5)
        h, w = stdscr.getmaxyx()
        y, x = int(h * 0.1), 0

        spawn = islands[0]
        spawn.make_visible()
        lt_y, lt_x, rb_y, rb_x = spawn.get_coordinates()
        hy, hx = (lt_y + rb_y) // 2, (lt_x + rb_x) // 2

        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j].get_type() == 'sea':
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(y + i, x + j, ' ')
                    stdscr.attroff(curses.color_pair(2))
                elif field[i][j].get_type() == 'ground':
                    stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(y + i, x + j, ' ')
                    stdscr.attroff(curses.color_pair(3))
                elif field[i][j].get_type() == 'bridge':
                    stdscr.attron(curses.color_pair(4))
                    stdscr.addstr(y + i, x + j, ' ')
                    stdscr.attroff(curses.color_pair(4))

                stdscr.refresh()

        objects['Hero'] = hero.Hero(hy, hx)

        while 1:
            for obj in objects:
                if obj == 'Hero':
                    t = 3 if field[hy][hx].get_type() == 'ground' else 4
                    stdscr.attron(curses.color_pair(t))
                    stdscr.addstr(y + hy, hx, '@')
                    stdscr.attroff(curses.color_pair(t))
            
            key = stdscr.getch()

            if key == ord('w') and field[hy - 1][hx].get_type() != 'sea':
                t = 3 if field[hy][hx].get_type() == 'ground' else 4
                del_foot(stdscr, y + hy, hx, t)
                hy -= 1
            elif key == ord('s') and field[hy + 1][hx].get_type() != 'sea':
                t = 3 if field[hy][hx].get_type() == 'ground' else 4
                del_foot(stdscr, y + hy, hx, t)
                hy += 1
            elif key == ord('a') and field[hy][hx - 1].get_type() != 'sea':
                t = 3 if field[hy][hx].get_type() == 'ground' else 4
                del_foot(stdscr, y + hy, hx, t)
                hx -= 1
            elif key == ord('d') and field[hy][hx + 1].get_type() != 'sea':
                t = 3 if field[hy][hx].get_type() == 'ground' else 4
                del_foot(stdscr, y + hy, hx, t)
                hx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break
            
            stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
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

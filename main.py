import curses
import time
from map_generator import map


menu = ['Play', 'Scoreboard', 'Exit']
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


def play(stdscr):
    levels = 1

    for _ in range(levels):
        field = map.generate_map(5)
        h, w = stdscr.getmaxyx()
        y = int(h * 0.1)
        x = 0

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

        while 1:
            key = stdscr.getch()

            if key == curses.KEY_ENTER or key in [10, 13]:
                break

def main(stdscr):
    curses.curs_set(0)
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

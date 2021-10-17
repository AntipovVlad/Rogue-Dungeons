import curses
from map_generator import map, map_elements
from game_objects import hero, enemy, bomb, stair
from random import randint, choice
from time import time


menu = ['Play', 'Scoreboard', 'Exit']
objects = {'Hero': None, 'Stair': None, 'Enemies': [], 'Bombs': [], 'Explosions': [], 'Coins': [], 'Boxes': []}
objects_coors = []

def print_menu(stdscr, selected_row_idx):
    global menu

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


def print_ending(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x = w // 2 - len(text) // 2
    y = h // 2 - 1

    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(y, x, text)
    stdscr.attroff(curses.color_pair(3))

    x = w // 2 - len("Enter 'e' to continue") // 2
    y = h // 2

    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(y, x, "Enter 'e' to continue")
    stdscr.attroff(curses.color_pair(3))
    
    stdscr.refresh()

def add_str(stdscr, y, x, s, t) -> None:
    stdscr.attron(curses.color_pair(t))
    stdscr.addstr(y, x, s)
    stdscr.attroff(curses.color_pair(t))


def out_objects(stdscr, field, st) -> None:
    global objects, objects_coors

    h, _ = stdscr.getmaxyx()
    y = int(h * 0.1)
    
    for obj in objects:
        if obj == 'Hero':
            hy, hx = objects['Hero'].get_coordinates()
            t = 4 if field[hy][hx].get_type() == 'room' else 1

            add_str(stdscr, y + hy, hx, objects['Hero'].get_skin(), t)
        elif obj == 'Stair':
            if objects[obj] is not None:
                sy, sx = objects['Stair'].get_coordinates()
                t = 117 + int(time() - st) % 5
                
                add_str(stdscr, y + sy, sx, objects['Stair'].get_skin(), t)
        else:
            for o in objects[obj]:
                oy, ox = o.get_coordinates()

                if obj == 'Bombs':
                    if int(time() - o.get_time()) > o.get_live():
                        objects[obj].remove(o)
                        objects['Explosions'].extend([bomb.Explosion(ey, ex, time()) for ey, ex in o.explode() if field[ey][ex].get_type() == 'room' and field[ey][ex].get_skin() == ' '])
                        objects_coors.remove(o.get_coordinates())

                        add_str(stdscr, y + oy, ox, ' ', 2)
                    else:
                        add_str(stdscr, y + oy, ox, o.get_skin(), 5 + int(time() - o.get_time()) % 2)
                if obj == 'Explosions':
                    if int(time() - o.get_time()) > o.get_live():
                        objects[obj].remove(o)

                        add_str(stdscr, y + oy, ox, ' ', 2)
                    else:
                        if objects['Hero'].get_coordinates() == (oy, ox):
                            objects['Hero'].de_health()
                            objects[obj].remove(o)

                        add_str(stdscr, y + oy, ox, o.get_skin(), 7)


def play(stdscr) -> None:
    global objects, objects_coors

    levels = 3
    h, _ = stdscr.getmaxyx()
    y = int(h * 0.1)

    for _ in range(levels):
        field, rooms, bridges = map.generate_map(5)
        start = time()
        finished = 0

        cur_room = rooms[0]
        cur_room.open()
        cur_room.activate()

        lt_y, lt_x, rb_y, rb_x = cur_room.get_coordinates()
        hy, hx = (lt_y + rb_y) // 2, (lt_x + rb_x) // 2

        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j].get_type() == 'stone':
                    add_str(stdscr, y + i, j, field[i][j].get_skin(), 117)
                elif field[i][j].get_type() == 'room':
                    add_str(stdscr, y + i, j, field[i][j].get_skin(), 4 if field[i][j].is_visible() else 117 + int(time() - start) % 5)

                stdscr.refresh()

        objects['Hero'] = hero.Hero(hy, hx)
        
        while 1:
            out_objects(stdscr, field, start)

            if objects['Hero'].is_dead():
                return False
            
            for i in range(len(field)):
                for j in range(len(field[0])):
                    if (field[i][j].get_type() == 'stone' or field[i][j].get_type() == 'room' and not field[i][j].is_visible()) and field[i][j].get_skin() in ['█', '╔', '╗', '╚', '╝']:
                        add_str(stdscr, y + i, j, field[i][j].get_skin(), 117 + int(time() - start) % 5)

            key = stdscr.getch()

            hy, hx = objects['Hero'].get_coordinates()

            for l, ny, nx in [['w', hy - 1, hx], ['s', hy + 1, hx], ['a', hy, hx - 1], ['d', hy, hx + 1]]:
                if key == ord(l) and field[ny][nx].get_skin() == ' ' and field[ny][nx].get_type() in ['room', 'bridge'] and (ny, nx) not in objects_coors:
                    t = 4 if field[hy][hx].get_type() == 'room' else 2
                    add_str(stdscr, y + hy, hx, field[hy][hx].get_skin(), t)
                    objects['Hero'].set_possintion(ny, nx)
                    hy, hx = ny, nx
                    
                    break
            
            for k, ny, nx in [[curses.KEY_UP, hy - 1, hx], [curses.KEY_DOWN, hy + 1, hx], [curses.KEY_LEFT, hy, hx - 1], [curses.KEY_RIGHT, hy, hx + 1]]:
                if key == k and field[ny][nx].get_skin() == ' ' and field[ny][nx].get_type() == 'room':
                    objects['Bombs'].append(bomb.Bomb(ny, nx, time()))
                    objects_coors.append((ny, nx))
                    
                    break
            
            if key == ord('o'):
                finished += 1
                if field[hy][hx].get_type() == 'room':
                    cur_room = field[hy][hx].get_zone()
                
                for dots, bridge in cur_room.open_bridges():
                    for dot in dots:
                        field[dot[0]][dot[1]] = map_elements.BridgeBlock(dot[0], dot[1], bridge)
                        field[dot[0]][dot[1]].make_visible()
                        field[dot[0]][dot[1]].set_activator([field[dot[0] - 1][dot[1]], field[dot[0] + 1][dot[1]], field[dot[0]][dot[1] - 1], field[dot[0]][dot[1] + 1]])
                            
                for i in range(len(field)):
                    for j in range(len(field[0])):
                        if field[i][j].get_type() == 'bridge':
                            t = 2 if field[i][j].is_visible() else 3
                        
                            add_str(stdscr, y + i, j, field[i][j].get_skin(), t)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break
            
            if field[hy][hx].get_type() == 'bridge' and field[hy][hx].activate():
                for i in range(len(field)):
                    for j in range(len(field[0])):
                        if field[i][j].get_type() == 'room':
                            t = 4 if field[i][j].is_visible() else 117 + int(time() - start) % 5
        
                            add_str(stdscr, y + i, j, field[i][j].get_skin(), t)
            
            if finished == len(rooms) and objects['Stair'] is None:
                lt_y, lt_x, rb_y, rb_x = cur_room.get_coordinates()

                sy, sx = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)
                while field[sy][sx].get_skin() != ' ':
                    sy, sx = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)

                objects['Stair'] = stair.Stair(sy, sx)
                
            if objects['Stair'] is not None and (hy, hx) == objects['Stair'].get_coordinates():
                break
                
            stdscr.refresh()
        
        field.clear()
        rooms.clear()
        bridges.clear()
        stdscr.clear()

        curses.beep()
    
    return True

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(1)
    stdscr.timeout(100)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(3, -1, -1)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    curses.init_pair(5, 234, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)

    curses.init_pair(7, 229, curses.COLOR_BLACK)


    for i in range(17, 22):
        curses.init_pair(100 + i, i, -1)

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
                fn = play(stdscr)

                if fn:
                    print_ending(stdscr, 'Congratilations! You won!')
                else:
                    print_ending(stdscr, 'Game over')
                
                while 1:
                    k = stdscr.getch()

                    if k == ord('e'):
                        break

            stdscr.clear()
            # stdscr.addstr(0, 0, f'You pressed {menu[current_row_idx]}')
            # stdscr.refresh()
            # stdscr.getch()
        
        print_menu(stdscr, current_row_idx)
        stdscr.refresh()


try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass

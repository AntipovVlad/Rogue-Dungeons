from map_generator import map, map_elements
from game_objects import hero, enemy, bomb, stair, coin, box
import curses
from random import randint
from time import time
from typing import Union


SCORE, LEVEL = 0, 0
menu = ['Play', 'Exit']

def print_menu(stdscr: object, selected_row_idx: int) -> None:
    """
    Printing game menu

    :param stdscr: screen
    :type stdscr: object
    :param selected_row_idx: index of selected option
    :type selected_row_idx: int
    
    :rtype: None
    :return: None
    """
    
    global menu
    screen = []
    mx_len = 0

    stdscr.clear()
    
    with open('start_screen.txt', 'r') as f:
        screen = [i.replace('\n', '') for i in f.readlines()]
        screen[0] = screen[0][1:]
    
    for i in range(len(screen)):
        mx_len = max(mx_len, len(screen[i]))

        for j in range(len(screen[i])):
            if screen[i][j] not in ['█', '▄', '▀']:
                add_str(stdscr, i, j, screen[i][j], 17)
            else:
                add_str(stdscr, i, j, screen[i][j], 121)
    
    h, w = stdscr.getmaxyx()

    c = len(sorted(menu, key=len, reverse=True)[0])
    a, b = len(menu) * 2 + 5, c * 2 + 9

    for i in range(a):
        for j in range(b):
            x = mx_len // 2 + w // 2 + j - c - 2
            y = h // 2 - len(menu) + i - 3

            wall = ''
            if j == b - 1: wall += 'r'
            if j == 0: wall += 'l'
            if i == a - 1: wall += 'b'
            if i == 0: wall += 't'
            sym = {'': ' ', 'l': '▌', 'r': '▐', 't': '▀', 'b': '▄', 'lt': '▛', 'rt': '▜', 'lb': '▙', 'rb': '▟'}[wall]

            add_str(stdscr, y, x, sym, 2)
    
    for idx, row in enumerate(menu):
        s = ' '.join(list(row.upper()))
        x = mx_len // 2 + w // 2 - c - 1
        y = h // 2 - len(menu) + idx * 2

        if idx == selected_row_idx:
            add_str(stdscr, y, x, ' ' + 'Ѫ' + ((b - len(s)) // 2 - 3) * ' '  + s + ((b - len(s)) // 2 - 3) * ' ' + 'Ѫ' + ' ', 1)
        else:
            add_str(stdscr, y, x, ((b - len(s)) // 2 - 1) * ' '  + s + ((b - len(s)) // 2 - 1) * ' ', 2)
    
    stdscr.refresh()


def print_ending(stdscr: object) -> None:
    """
    Printing ending text

    :param stdscr: screen
    :type stdscr: object
    :param text: end text
    :type text: str
    
    :rtype: None
    :return: None
    """
    global SCORE

    stdscr.clear()    
    
    h, w = stdscr.getmaxyx()

    for i in range(h):
        for j in range(w):
            stdscr.attron(curses.color_pair(3))
            stdscr.insch(i, j, ' ')
            stdscr.attroff(curses.color_pair(3))

    x = w // 2 - len(f'Game over. Your score: {SCORE}') // 2
    y = h // 2 - 1

    add_str(stdscr, y, x, f'Game over. Your score: {SCORE}', 3)

    x = w // 2 - len("Enter 'e' to continue") // 2
    y = h // 2

    add_str(stdscr, y, x, 'Enter "e" to continue', 3)

    
    stdscr.refresh()


def add_str(stdscr: object, y: int, x: int, s: str, t: int) -> None:
    """
    'Fish' for screen output

    :param stdscr: screen
    :type stdscr: object
    :param y: y coordinate
    :type y: int
    :param x: x coordinate
    :type x: int
    :param s: text
    :type s: str
    :param t: color type
    :type t: int
    
    :rtype: None
    :return: None
    """
    
    stdscr.attron(curses.color_pair(t))
    stdscr.addstr(y, x, s)
    stdscr.attroff(curses.color_pair(t))


def create_object(tp: str, objects_coors: dict, field: list, extra_params: dict) -> None:
    """
    Creation of new game object

    :param tp: name of object
    :type tp: str
    :param object_coors: coordinates of new game object
    :type object_coors: dict
    :param field: map array
    :type field: list
    :param extra_params: additional parameters
    :type extra_params: dict

    :rtype: None
    :return: None
    """
    
    global SCORE

    if tp == 'bomb':
        coors = extra_params['coors']
        hero = extra_params['hero']

        if field[coors[0]][coors[1]].get_skin() == ' ' and field[coors[0]][coors[1]].get_type() == 'room' and objects_coors.get(coors) is None:
            if hero.get_bombs() > 0:
                hero.de_bombs()
                objects_coors[coors] = bomb.Bomb(coors[0], coors[1], time())
    if tp == 'expl':
        coors = extra_params['coors']

        if field[coors[0]][coors[1]].get_skin() == ' ' and field[coors[0]][coors[1]].get_type() in ['room', 'bridge']:
            if objects_coors.get(coors) is None:
                objects_coors[coors] = bomb.Explosion(coors[0], coors[1], time())
            
            elif objects_coors.get(coors) is not None and objects_coors[coors].get_type() == 'hero':
                objects_coors[coors].de_health()
            
            elif objects_coors.get(coors) is not None and objects_coors[coors].get_type() == 'enemy':
                if objects_coors[coors].de_health(objects_coors):
                    SCORE += 100
            
            elif objects_coors.get(coors) is not None and objects_coors[coors].get_type() == 'box':
                if randint(0, 100) % 10 == 0:
                    objects_coors[coors] = coin.Coin(coors[0], coors[1])
                else:
                    objects_coors.pop(coors)
            
            elif objects_coors.get(coors) is not None and objects_coors[coors].get_type() == 'coin':
                objects_coors.pop(coors)
    if tp in ['stair', 'coin', 'box']:
        room = extra_params['room']

        lt_y, lt_x, rb_y, rb_x = room.get_coordinates()

        y, x = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)
        while field[y][x].get_skin() != ' ' or objects_coors.get((y, x)) is not None:
            y, x = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)

        if tp == 'stair':
            objects_coors[(y, x)] = stair.Stair(y, x)
        elif tp == 'coin':
            objects_coors[(y, x)] = coin.Coin(y, x)
        elif tp == 'box':
            objects_coors[(y, x)] = box.Box(y, x)


def check_collitions(hero: hero.Hero, objects_coors: dict, field: list, coors: tuple) -> bool:
    """
    Replacement of hero

    :param hero: Hero object
    :type hero: hero.Hero
    :param objects_coors: dictinary of coordinates and their objects
    :type objects_coors: dict
    :param field: map array
    :type field: list
    :param coors: coordinates of hero
    :type coors: tuple
    
    :rtype: bool
    :return: whether hero found exit or not
    """
    
    global SCORE

    if field[coors[0]][coors[1]].get_skin() == ' ' and field[coors[0]][coors[1]].get_type() == 'room' or field[coors[0]][coors[1]].get_type() == 'bridge':
        if objects_coors.get(coors) is None:
            py, px = hero.get_coordinates()
            objects_coors.pop((py, px))

            objects_coors[coors] = hero
            hero.set_possintion(coors[0], coors[1])        
        elif objects_coors[coors].get_type() == 'stair':
            py, px = hero.get_coordinates()
            objects_coors.pop((py, px))

            objects_coors[coors] = hero
            hero.set_possintion(coors[0], coors[1])
            
            return True
        elif objects_coors[coors].get_type() == 'enemy':
            hero.de_health()
            objects_coors[coors].set_freeze()
        elif objects_coors[coors].get_type() == 'coin':
            py, px = hero.get_coordinates()
            objects_coors.pop((py, px))

            hero.set_possintion(coors[0], coors[1])
            SCORE += 10
            
            objects_coors[coors] = hero
        elif objects_coors[coors].get_type() == 'expl':
            py, px = hero.get_coordinates()
            objects_coors.pop((py, px))

            hero.set_possintion(coors[0], coors[1])
            hero.de_health()
            
            objects_coors[coors] = hero

    return False


def activate_room(room: map_elements.Room, objects_coors: dict, field: list, enemies: set) -> None:
    """
    Makes room active

    :param room: room object
    :type room: map_elements.Room
    :param object_coors: dictinary of coordinates and their objects
    :type object_coors: dict
    :param field: map array
    :type field: list
    :param enemies: array of room enemies
    :type enemies: list

    :rtype: None
    :return: None
    """
    global LEVEL
    
    if not room.is_activated():
        lt_y, lt_x, rb_y, rb_x = room.get_coordinates()
        room_enemies = []
        coins, ens, boxes, S = 0, 0, 0, (rb_y - lt_y) * (rb_x - lt_x)
        if S <= 500:
            coins, ens, boxes = 2, 1, 4
        elif S <= 1000:
            coins, ens, boxes = 4, 2, 6
        elif S <= 1500:
            coins, ens, boxes = 6, 3, 8
        else:
            coins, ens, boxes = 8, 4, 10

        for _ in range(coins):
            create_object('coin', objects_coors, field, {'room' : room})
        
        for _ in range(boxes):
            create_object('box', objects_coors, field, {'room' : room})

        for _ in range(ens):
            by, bx = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)
            en = enemy.Snake(by, bx, room, LEVEL)
            while not en.can_extist(field, objects_coors):
                by, bx = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)
                en = enemy.Snake(by, bx, room, LEVEL)
            
            en.set_freeze()

            for coors in en.get_coordinates():
                objects_coors[coors] = en
            
            room_enemies.append(en)
            enemies.add(en)
        
        room.activate(room_enemies)


def action(enemies: set, objects_coors: dict, field: list, hero: hero.Hero) -> None:
    """
    Changing objects' statements

    :param enemies: array of enemies
    :type enemies: set
    :param object_coors: dictinary of coordinates and their objects
    :type object_coors: dict
    :param field: map array
    :type field: list
    :param hero: Hero object
    :type hero: hero.Hero

    :rtype: None
    :return: None
    """
    
    c_objects_coors = objects_coors.copy()

    for coors in c_objects_coors:
        obj = c_objects_coors[coors]

        if obj.get_type() == 'bomb':
            if int(time() - obj.get_time()) > obj.get_live():
                objects_coors.pop(obj.get_coordinates())
                hero.in_bombs()
                
                for ey, ex in obj.explode():
                    create_object('expl', objects_coors, field, {'coors': (ey, ex)})
        if obj.get_type() == 'expl':
            if int(time() - obj.get_time()) > obj.get_live():
                objects_coors.pop(obj.get_coordinates())
        if obj.get_type() == 'coin':
            obj.blink()

    c_enemies = enemies.copy()
    for en in c_enemies:
        if en.get_health() < 1:
            enemies.remove(en)
            en.get_room().del_enemy(en)
            continue

        en.de_freeze()
        en.change_direction()

        if not en.is_freeze():
            en.move(field, objects_coors, hero)


def out_info(stdscr: object, hero: hero.Hero) -> None:
    """
    Outputs game information

    :param stdscr: screen
    :type stdscr: object
    :param hero: Hero object
    :type hero: hero.Hero

    :rtype: None
    :return: None
    """

    global SCORE, LEVEL
    
    h, w = stdscr.getmaxyx()
    frazes = [(1, 'HP: ', 10), (5, '♥ ' * hero.get_hp(), 9), (w // 2 - len(f'Score: {SCORE}') // 2, f'Score: {SCORE}', 10), (w - 2 - len(f'Level: {LEVEL}'), f'Level: {LEVEL}', 10)]
    y = int(h * 0.1)

    for i in list(range(y)) + list(range(h - y - 1, h)):
        for j in range(w):
            stdscr.attron(curses.color_pair(10))
            stdscr.insch(i, j, ' ')
            stdscr.attroff(curses.color_pair(10))
    
    y = 1
    for f in frazes:
        add_str(stdscr, y, f[0], f[1], f[2])

    stdscr.refresh()


def out_map(stdscr: object, field: list, start: float) -> None:
    """
    Outputs map

    :param stdscr: screen
    :type stdscr: object
    :param field: map array
    :type field: list
    :param start: time, when game started
    :type start: float

    :rtype: None
    :return: None
    """
    
    h, _ = stdscr.getmaxyx()
    y = int(h * 0.1)

    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j].get_type() == 'stone':
                add_str(stdscr, y + i, j, field[i][j].get_skin(), 117 + int(time() - start) % 5)
            elif field[i][j].get_type() == 'room':                
                if not field[i][j].is_visible():
                    t = 117 + int(time() - start) % 5
                else:
                    t = 2
                add_str(stdscr, y + i, j, field[i][j].get_skin(), t)
            elif field[i][j].get_type() == 'bridge':
                if field[i][j].is_visible():
                    if field[i][j].get_room() is not None:
                        if not field[i][j].get_room().is_activated():
                            add_str(stdscr, y + i, j, field[i][j].get_skin(), 3)
                    else:
                        add_str(stdscr, y + i, j, field[i][j].get_skin(), 12)
                else:
                    add_str(stdscr, y + i, j, field[i][j].get_skin(), 3)
    
    stdscr.refresh()


def out_objects(stdscr: object, field: list, objects_coors: dict) -> None:
    """
    Outputs game objects

    :param stdscr: screen
    :type stdscr: object
    :param field: map array
    :type field: list
    :param object_coors: dictinary of coordinates and their objects
    :type object_coors: dict

    :rtype: None
    :return: None
    """
    
    h, _ = stdscr.getmaxyx()
    y = int(h * 0.1)
    
    c_objects_coors = objects_coors.copy()

    for coors in c_objects_coors:
        obj = c_objects_coors[coors]

        if obj.get_type() == 'hero':
            t, s = 15 if field[coors[0]][coors[1]].get_type() == 'room' else 12, obj.get_skin()
        elif obj.get_type() == 'stair':
            t, s = 203, obj.get_skin()
        elif obj.get_type() == 'bomb':
            t, s = 5 + int(time() - obj.get_time()) % 2, obj.get_skin()
        elif obj.get_type() == 'expl':
            t, s = 7, obj.get_skin()
        elif obj.get_type() == 'enemy':
            t, s = 14, obj.get_skin()
        elif obj.get_type() == 'coin':
            t, s = 13, obj.get_skin()
        elif obj.get_type() == 'box':
            t, s = 18, obj.get_skin()
        
        add_str(stdscr, y + coors[0], coors[1], s, t)
    
    stdscr.refresh()


def play(stdscr: object) -> Union[bool, None]:
    """
    Main levels' cycle

    :param stdscr: screen
    :type stdscr: object

    :rtype: bool or None
    :return: win or loose, can't start
    """
    
    global LEVEL

    LEVEL = 0

    levels = 1024

    for _ in range(levels):
        LEVEL += 1
        objects_coors = {}
        enemies = set()
        c_exit = False

        field, rooms, bridges = map.generate_map(5)
        
        start = time()
        cleared = 0

        cur_room = rooms[0]
        cur_room.open()

        lt_y, lt_x, rb_y, rb_x = cur_room.get_coordinates()
        hy, hx = (lt_y + rb_y) // 2, (lt_x + rb_x) // 2
        H = hero.Hero(hy, hx)
        objects_coors[(hy, hx)] = H

        activate_room(cur_room, objects_coors, field, enemies)

        while not c_exit:
            if H.is_dead():
                return False
            
            action(enemies, objects_coors, field, H)

            out_info(stdscr, H)
            out_map(stdscr, field, start)
            out_objects(stdscr, field, objects_coors)

            key = stdscr.getch()

            hy, hx = H.get_coordinates()

            for l, ny, nx in [['w', hy - 1, hx], ['s', hy + 1, hx], ['a', hy, hx - 1], ['d', hy, hx + 1]]:
                if key == ord(l):
                    command = check_collitions(H, objects_coors, field, (ny, nx))
                    if command:
                        c_exit = True
                        out_map(stdscr, field, start)
                        out_objects(stdscr, field, objects_coors)
                        stdscr.refresh()

                    hy, hx = H.get_coordinates()
                    cur_room = cur_room if field[hy][hx].get_type() == 'bridge' else field[hy][hx].get_zone()
                    enemies.update(cur_room.get_enemies())
                    
                    break
                                
            for k, ny, nx in [[curses.KEY_UP, hy - 1, hx], [curses.KEY_DOWN, hy + 1, hx], [curses.KEY_LEFT, hy, hx - 1], [curses.KEY_RIGHT, hy, hx + 1]]:
                if key == k:
                    create_object('bomb', objects_coors, field, {'coors': (ny, nx), 'hero': H})
                    
                    break
            
            if key == curses.KEY_ENTER or key in [10, 13]:
                c_objects_coors = objects_coors.copy()

                for coors in c_objects_coors:
                    obj = c_objects_coors[coors]
                    if obj.get_type() == 'bomb':
                        objects_coors.pop(obj.get_coordinates())
                        H.in_bombs()
                        
                        for ey, ex in obj.explode():
                            create_object('expl', objects_coors, field, {'coors': (ey, ex)})
            
            if not cur_room.is_cleared() and len(cur_room.get_enemies()) == 0:
                cleared += 1

                cur_room.clear()
                
                for dots, bridge in cur_room.open_bridges():
                    for dot in dots:
                        field[dot[0]][dot[1]] = map_elements.BridgeBlock(dot[0], dot[1], bridge)
                        field[dot[0]][dot[1]].make_visible()
                        if not field[dot[0]][dot[1]].set_activator([field[dot[0] - 1][dot[1]], field[dot[0] + 1][dot[1]], field[dot[0]][dot[1] - 1], field[dot[0]][dot[1] + 1]]):
                            field[dot[0]][dot[1]] = map_elements.RoomBlock(dot[0], dot[1], cur_room, '')
                            field[dot[0]][dot[1]].make_visible()
                
                if cleared == len(rooms):
                    create_object('stair', objects_coors, field, {'room': cur_room})
            
            if field[hy][hx].get_type() == 'bridge':
                if field[hy][hx].activate():
                    opened_room = field[hy][hx].get_room()
                    activate_room(opened_room, objects_coors, field, enemies)

                    field[hy][hx] = map_elements.RoomBlock(hy, hx, opened_room, '')
                    field[hy][hx].make_visible()               
                
            stdscr.refresh()
        
        field.clear()
        rooms.clear()
        bridges.clear()
        stdscr.clear()

        curses.beep()
    
    return True

def init_curses() -> None:
    """
    Initializes colors

    :rtype: None
    :return: None
    """
    
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    # ======== Menu ========
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    # ======== Field ========
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, 233)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(11, 12, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_BLACK, 12)
    curses.init_pair(16, 233, curses.COLOR_WHITE)
    #curses.init_pair(19, 233, curses.COLOR_WHITE)

    # ======== Bombs ========
    curses.init_pair(5, 21, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # ======== Explosion ========
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # ======== Info board ========
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_RED, 233)
    curses.init_pair(10, curses.COLOR_WHITE, 233)

    # ======== Blinking stones ========
    for i in range(17, 22):
        curses.init_pair(100 + i, i, 233)
    
    # ======== Coins ========
    curses.init_pair(13, 11, curses.COLOR_BLACK)

    # ======== Snake ========
    curses.init_pair(14, curses.COLOR_CYAN + 8, curses.COLOR_BLACK)

    # ======== Hero ========
    curses.init_pair(15, curses.COLOR_GREEN + 8, curses.COLOR_BLACK)
    curses.init_pair(17, curses.COLOR_GREEN + 8, -1)

    # ======== Boxes ========
    curses.init_pair(18, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    # ======== Exit ========
    curses.init_pair(203, 203, curses.COLOR_BLACK)


def main(stdscr: object) -> None:
    """
    Game loop

    :param stdscr: screen
    :type stdscr: object
    """
    
    stdscr.nodelay(1)
    stdscr.timeout(100)

    init_curses()

    current_row_idx = 0
    
    print_menu(stdscr, current_row_idx)
        
    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu[current_row_idx] == 'Exit':
                break
            
            if menu[current_row_idx] == 'Play':
                play(stdscr)

                print_ending(stdscr)

                while 1:
                    k = stdscr.getch()

                    if k == ord('e'):
                        break

            stdscr.clear()
        
        print_menu(stdscr, current_row_idx)
        stdscr.refresh()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except curses.error:
        print('Make terminal size bigger!')

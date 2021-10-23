import curses
from map_generator import map, map_elements
from game_objects import hero, enemy, bomb, stair, coin
from random import randint, choice
from time import time, sleep


SCORE = 0
menu = ['Play', 'Scoreboard', 'Exit']

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


def create_object(tp: str, objects_coors: dict, field: list, extra_params: dict) -> None:
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
            
            if objects_coors.get(coors) is not None and objects_coors[coors].get_type() == 'hero':
                objects_coors[coors].de_health()
            
            if objects_coors.get(coors) is not None and objects_coors[coors].get_type() == 'enemy':
                if objects_coors[coors].de_health(objects_coors):
                    SCORE += 100
            
            if objects_coors.get(coors) is not None and objects_coors[coors].get_type() == 'box':
                pass

            if objects_coors.get(coors) is not None and objects_coors[coors].get_type() == 'coin':
                objects_coors.pop(coors)
    if tp in ['stair', 'coin']:
        room = extra_params['room']

        lt_y, lt_x, rb_y, rb_x = room.get_coordinates()

        y, x = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)
        while field[y][x].get_skin() != ' ' or objects_coors.get((y, x)) is not None:
            y, x = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)

        objects_coors[(y, x)] = stair.Stair(y, x) if tp == 'stair' else coin.Coin(y, x)


def check_collitions(hero, objects_coors, field, coors) -> bool:
    global SCORE

    if field[coors[0]][coors[1]].get_skin() == ' ' and field[coors[0]][coors[1]].get_type() in ['room', 'bridge']:
        if objects_coors.get(coors) is None:
            py, px = hero.get_coordinates()
            objects_coors.pop((py, px))

            objects_coors[coors] = hero
            hero.set_possintion(coors[0], coors[1])

            return False
        
        if objects_coors[coors].get_type() == 'stair':
            py, px = hero.get_coordinates()
            objects_coors.pop((py, px))

            objects_coors[coors] = hero
            hero.set_possintion(coors[0], coors[1])
            
            return True
        
        if objects_coors[coors].get_type() == 'enemy':
            hero.de_health()
            objects_coors[coors].set_freeze()
            # add freeze and blink
        
        if objects_coors[coors].get_type() == 'coin':
            py, px = hero.get_coordinates()
            objects_coors.pop((py, px))

            hero.set_possintion(coors[0], coors[1])
            SCORE += 10
            
            objects_coors[coors] = hero
        
        if objects_coors[coors].get_type() == 'expl':
            py, px = hero.get_coordinates()
            objects_coors.pop((py, px))

            hero.set_possintion(coors[0], coors[1])
            hero.de_health()
            
            objects_coors[coors] = hero

    return False


def activate_room(room, objects_coors, field, enemies: list) -> None:
    if not room.is_activated():
        lt_y, lt_x, rb_y, rb_x = room.get_coordinates()
        room_enemies = []
        coins, ens, S = 0, 0, (rb_y - lt_y) * (rb_x - lt_x)
        if S <= 500:
            coins = 2
            ens = 1
        elif S <= 1000:
            coins = 4
            ens = 2
        elif S <= 1500:
            coins = 6
            ens = 3
        else:
            coins = 8
            ens = 4

        for _ in range(coins):
            create_object('coin', objects_coors, field, {'room' : room})

        for _ in range(ens):
            by, bx = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)
            en = enemy.Snake(by, bx, room)
            while not en.can_extist(field, objects_coors):
                by, bx = randint(lt_y + 1, rb_y - 1), randint(lt_x + 1, rb_x - 1)
                en = enemy.Snake(by, bx, room)
            
            en.set_freeze()

            for coors in en.get_coordinates():
                objects_coors[coors] = en
            
            room_enemies.append(en)
            enemies.add(en)
        
        room.activate(room_enemies)


def move(enemies, objects_coors, field, hero) -> None:
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


def out_info(stdscr, hero) -> None:
    global SCORE

    h, w = stdscr.getmaxyx()
    y = int(h * 0.1)

    for i in list(range(y)) + list(range(h - y, h)):
        for j in range(w):
            stdscr.attron(curses.color_pair(10))
            stdscr.insch(i, j, ' ')
            stdscr.attroff(curses.color_pair(10))
    
    y, x = 1, 1
    add_str(stdscr, y, x, 'HP: ', 10)
    
    x += 4
    add_str(stdscr, y, x, '♥ ' * hero.get_hp(), 9)
    
    x += hero.get_hp() * 2 - 1

    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(y, x, ' ' * (hero.get_hp() - hero.get_hp()))
    stdscr.attroff(curses.color_pair(3))

    x = w // 2 - len(f'Score: {SCORE}') // 2
    stdscr.attron(curses.color_pair(10))
    stdscr.addstr(y, x, f'Score: {SCORE}')
    stdscr.attroff(curses.color_pair(10))

    stdscr.refresh()


def out_map(stdscr, field, start) -> None:
    h, _ = stdscr.getmaxyx()
    y = int(h * 0.1)

    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j].get_type() == 'stone':
                add_str(stdscr, y + i, j, field[i][j].get_skin(), 117 + int(time() - start) % 5)
            elif field[i][j].get_type() == 'room':
                add_str(stdscr, y + i, j, field[i][j].get_skin(), 4 if field[i][j].is_visible() else 117 + int(time() - start) % 5)
            elif field[i][j].get_type() == 'bridge':            
                add_str(stdscr, y + i, j, field[i][j].get_skin(), 2 if field[i][j].is_visible() else 3)
    
    stdscr.refresh()


def out_objects(stdscr, field, objects_coors, hero) -> None:
    h, _ = stdscr.getmaxyx()
    y = int(h * 0.1)
    
    c_objects_coors = objects_coors.copy()

    for coors in c_objects_coors:
        obj = c_objects_coors[coors]

        if obj.get_type() == 'hero':
            t, s = 4 if field[coors[0]][coors[1]].get_type() == 'room' else 1, obj.get_skin()
        elif obj.get_type() == 'stair':
            t, s = 203, obj.get_skin()
        elif obj.get_type() == 'bomb':
            t, s = 5 + int(time() - obj.get_time()) % 2, obj.get_skin()
        elif obj.get_type() == 'expl':
            t, s = 7, obj.get_skin()
        elif obj.get_type() == 'enemy':
            t, s = 4, obj.get_skin()
        elif obj.get_type() == 'coin':
            t, s = 11, obj.get_skin()
        
        add_str(stdscr, y + coors[0], coors[1], s, t)
    
    stdscr.refresh()


def play(stdscr) -> None:
    levels = 10

    for _ in range(levels):
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
            
            move(enemies, objects_coors, field, H)

            out_info(stdscr, H)
            out_map(stdscr, field, start)
            out_objects(stdscr, field, objects_coors, H)

            key = stdscr.getch()

            hy, hx = H.get_coordinates()

            for l, ny, nx in [['w', hy - 1, hx], ['s', hy + 1, hx], ['a', hy, hx - 1], ['d', hy, hx + 1]]:
                if key == ord(l):
                    command = check_collitions(H, objects_coors, field, (ny, nx))
                    if command:
                        c_exit = True
                        out_map(stdscr, field, start)
                        out_objects(stdscr, field, objects_coors, H)
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
                        field[dot[0]][dot[1]].set_activator([field[dot[0] - 1][dot[1]], field[dot[0] + 1][dot[1]], field[dot[0]][dot[1] - 1], field[dot[0]][dot[1] + 1]])
                
                if cleared == len(rooms):
                    create_object('stair', objects_coors, field, {'room': cur_room})
            
            if field[hy][hx].get_type() == 'bridge':
                if field[hy][hx].activate():
                    opened_room = field[hy][hx].get_room().get_zone()

                    activate_room(opened_room, objects_coors, field, enemies)                    
                
            stdscr.refresh()
        
        field.clear()
        rooms.clear()
        bridges.clear()
        stdscr.clear()

        curses.beep()
    
    return True

def init_curses():
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    # ======== Field ========
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(3, -1, -1)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # ======== Bombs ========
    curses.init_pair(5, 21, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # ======== Explosion ========
    curses.init_pair(7, 229, curses.COLOR_BLACK)
    
    # ======== Info board ========
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_RED, 233)
    curses.init_pair(10, curses.COLOR_WHITE, 233)

    # ======== Blinking stones ========
    for i in range(17, 22):
        curses.init_pair(100 + i, i, -1)
    
    # ======== Coins ========
    curses.init_pair(11, 12, curses.COLOR_BLACK)
    
    # ======== Exit ========
    curses.init_pair(203, 203, curses.COLOR_BLACK)

def main(stdscr):
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
        
        print_menu(stdscr, current_row_idx)
        stdscr.refresh()


try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass

import unittest
import main
from map_generator import map, map_elements
from game_objects import hero, enemy, box, coin, stair, bomb
import pickle
from time import sleep, time
import curses



with open('test_map.txt', 'rb') as f:
    field, rooms, bridges = pickle.load(f)

rt = map_elements.Room([(0, 0), (3, 3)])


class MainTest(unittest.TestCase):
    def testCreateObject(self):
        ff = [
            [map_elements.RoomBlock(0, 0, rt, 'lt'), map_elements.RoomBlock(0, 1, rt, 't'), map_elements.RoomBlock(0, 2, rt, 't'), map_elements.RoomBlock(0, 3, rt, 'rt')],
            [map_elements.RoomBlock(1, 0, rt, 'l'), map_elements.RoomBlock(1, 1, rt, ''), map_elements.RoomBlock(1, 2, rt, ''), map_elements.RoomBlock(1, 3, rt, 'r')],
            [map_elements.RoomBlock(2, 0, rt, 'l'), map_elements.RoomBlock(2, 1, rt, ''), map_elements.RoomBlock(2, 2, rt, ''), map_elements.RoomBlock(2, 3, rt, 'r')],
            [map_elements.RoomBlock(3, 0, rt, 'lb'), map_elements.RoomBlock(3, 1, rt, 'b'), map_elements.RoomBlock(3, 2, rt, 'b'), map_elements.RoomBlock(3, 3, rt, 'rb')]
        ]
        objects_coors = {}
        H = hero.Hero(2, 1)
        objects_coors[(2, 1)] = H
        
        b = H.get_bombs()
        main.create_object('bomb', objects_coors, ff, {'coors': (1, 1), 'hero': H})
        self.assertEqual(H.get_bombs(), b - 1)
        self.assertIsNotNone(objects_coors.get((1, 1)))
        self.assertEqual(objects_coors.get((1, 1)).get_type(), 'bomb')
        
        objects_coors.pop((1, 1))

        main.create_object('expl', objects_coors, ff, {'coors': (1, 2)})
        self.assertIsNotNone(objects_coors.get((1, 2)))
        self.assertEqual(objects_coors.get((1, 2)).get_type(), 'expl')

        objects_coors.pop((1, 2))
        
        h = H.get_hp()
        main.create_object('expl', objects_coors, ff, {'coors': (2, 1)})
        self.assertEqual(objects_coors.get((2, 1)).get_type(), 'hero')
        self.assertEqual(h - H.get_hp(), 1)

        objects_coors.pop((2, 1))

        en = enemy.Snake(1, 2, rt)
        
        for coors in en.get_coordinates():
            objects_coors[coors] = en
        en.de_health(objects_coors)
        h = en.get_health()
        main.create_object('expl', objects_coors, ff, {'coors': (1, 2)})
        self.assertIsNone(objects_coors.get((1, 1)))
        self.assertEqual(h - en.get_health(), 1)

        objects_coors.pop((1, 2))

        objects_coors[(1, 1)] = box.Box(1, 1)
        main.create_object('expl', objects_coors, ff, {'coors': (1, 1)})
        self.assertIn(type(objects_coors.get((1, 1))).__name__, ['NoneType', 'Coin'])

        if objects_coors.get((1, 1)) is not None:
            objects_coors.pop((1, 1))
        
        objects_coors[(1, 1)] = coin.Coin(1, 1)
        main.create_object('expl', objects_coors, ff, {'coors': (1, 1)})
        self.assertIsNone(objects_coors.get((1, 1)))

        for k in ['stair', 'coin', 'box']:
            main.create_object(k, objects_coors, ff, {'room': rt})
            flag = False
            y, x = 0, 0
            for i in range(4):
                for j in range(4):
                    if objects_coors.get((i, j)) is not None and objects_coors.get((i, j)).get_type() == k:
                        y, x = i, j
                        flag = True
            
            self.assertTrue(flag)
            objects_coors.pop((y, x))

    def testChechCollisions(self):
        ff = [
            [map_elements.RoomBlock(0, 0, rt, 'lt'), map_elements.RoomBlock(0, 1, rt, 't'), map_elements.RoomBlock(0, 2, rt, 't'), map_elements.RoomBlock(0, 3, rt, 'rt')],
            [map_elements.RoomBlock(1, 0, rt, 'l'), map_elements.RoomBlock(1, 1, rt, ''), map_elements.RoomBlock(1, 2, rt, ''), map_elements.RoomBlock(1, 3, rt, 'r')],
            [map_elements.RoomBlock(2, 0, rt, 'l'), map_elements.RoomBlock(2, 1, rt, ''), map_elements.RoomBlock(2, 2, rt, ''), map_elements.RoomBlock(2, 3, rt, 'r')],
            [map_elements.RoomBlock(3, 0, rt, 'lb'), map_elements.RoomBlock(3, 1, rt, 'b'), map_elements.RoomBlock(3, 2, rt, 'b'), map_elements.RoomBlock(3, 3, rt, 'rb')]
        ]
        objects_coors = {}
        H = hero.Hero(2, 1)
        objects_coors[(2, 1)] = H

        main.check_collitions(H, objects_coors, ff, (1, 1))
        self.assertEqual(objects_coors.get((1, 1)).get_type(), 'hero')

        main.check_collitions(H, objects_coors, ff, (1, 0))
        self.assertEqual(objects_coors.get((1, 1)).get_type(), 'hero')

        objects_coors[(2, 1)] = stair.Stair(2, 1)
        self.assertTrue(main.check_collitions(H, objects_coors, ff, (2, 1)))

        h = H.get_hp()
        en = enemy.Snake(1, 2, rt)
        
        for coors in en.get_coordinates():
            objects_coors[coors] = en
        main.check_collitions(H, objects_coors, ff, (1, 1))
        self.assertEqual(h - H.get_hp(), 1)

        for _ in range(3):
            en.de_health(objects_coors)
        
        objects_coors[(1, 1)] = coin.Coin(1, 1)
        main.check_collitions(H, objects_coors, ff, (1, 1))
        self.assertEqual(objects_coors.get((1, 1)).get_type(), 'hero')

        objects_coors[(2, 1)] = bomb.Explosion(2, 1, time())
        h = H.get_hp()
        main.check_collitions(H, objects_coors, ff, (2, 1))
        self.assertEqual(objects_coors.get((2, 1)).get_type(), 'hero')
        self.assertEqual(h - H.get_hp(), 1)

    def testRoomActivation(self):
        global rooms, field
        objects_coors = {}
        enemies = set()

        main.activate_room(rooms[0], objects_coors, field, enemies)
        self.assertTrue(rooms[0].is_activated())

    def testMapGenerating(self):
        self.assertLessEqual(len(map.generate_map(5)[1]), 5)


if __name__ == '__main__':
    unittest.main()

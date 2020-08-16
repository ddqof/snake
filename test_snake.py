#!/usr/bin/env python3

import unittest
import snake_engine
import snake_components
import os
from snake_components import Point


class SnakeMove(unittest.TestCase):
    def setUp(self):
        level = os.path.join('.test_levels', 'move')
        self.engine = snake_engine.Driver(level, None)

    def move_and_get_snake_coords(self, count):
        for i in range(count):
            self.engine.snake.move()
        coords = []
        for block in self.engine.snake.blocks:
            coords.append(block.map_coords)
        return coords

    def test_move_right_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(1, 0)
        result = self.move_and_get_snake_coords(1)
        expected = [Point(11, 13), Point(10, 13), Point(9, 13), Point(8, 13), Point(7, 13), Point(6, 13)]
        self.assertListEqual(expected, result)

    def test_move_up_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(0, -1)
        result = self.move_and_get_snake_coords(1)
        expected = [Point(10, 12), Point(10, 13), Point(9, 13), Point(8, 13), Point(7, 13), Point(6, 13)]
        self.assertListEqual(expected, result)

    def test_move_down_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        result = self.move_and_get_snake_coords(1)
        expected = [Point(10, 14), Point(10, 13), Point(9, 13), Point(8, 13), Point(7, 13), Point(6, 13)]
        self.assertListEqual(expected, result)

    def test_move_down_for_three_blocks(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        result = self.move_and_get_snake_coords(3)
        expected = [Point(10, 16), Point(10, 15), Point(10, 14), Point(10, 13), Point(9, 13), Point(8, 13)]
        self.assertListEqual(expected, result)

    def test_difficult_path(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(0, -1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(0, -1)
        self.engine.snake.move()
        result = self.move_and_get_snake_coords(0)
        expected = [Point(12, 12), Point(12, 13), Point(11, 13), Point(11, 14), Point(10, 14), Point(10, 13)]
        self.assertListEqual(expected, result)
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        result = self.move_and_get_snake_coords(4)
        expected = [Point(8, 12), Point(9, 12), Point(10, 12), Point(11, 12), Point(12, 12), Point(12, 13)]
        self.assertListEqual(expected, result)

    def test_bounds(self):
        self.engine.snake.vector = snake_components.Vector(0, -1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        for i in range(11):
            self.engine.snake.move()
        self.engine.snake.check_walls()
        result = self.move_and_get_snake_coords(0)
        expected = [Point(39, 12), Point(0, 12), Point(1, 12), Point(2, 12), Point(3, 12), Point(4, 12)]
        self.assertTrue(self.engine.in_game)
        self.assertListEqual(expected, result)
        result = self.move_and_get_snake_coords(1)
        expected = [Point(38, 12), Point(39, 12), Point(0, 12), Point(1, 12), Point(2, 12), Point(3, 12)]
        self.assertListEqual(expected, result)

    def test_self_eating(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(0, -1)
        result = self.move_and_get_snake_coords(1)
        expected = [Point(9, 13), Point(9, 14), Point(10, 14), Point(10, 13), Point(9, 13), Point(8, 13)]
        self.engine.snake.check_self_eating()
        self.assertFalse(self.engine.in_game)
        self.assertListEqual(expected, result)
        self.engine.snake.move()
        self.assertListEqual(expected, result)


class SnakeInteractionsWithMap(unittest.TestCase):

    def move_and_get_snake_coords(self, count):
        for i in range(count):
            self.engine.snake.move()
        coords = []
        for block in self.engine.snake.blocks:
            coords.append(block.map_coords)
        return coords

    def test_interact_with_default_food(self):
        level = os.path.join('.test_levels', 'default_food')
        self.engine = snake_engine.Driver(level, None)
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.check_food()
        result = self.move_and_get_snake_coords(1)
        expected = [Point(12, 13), Point(11, 13), Point(10, 13), Point(9, 13),
                    Point(8, 13), Point(7, 13), Point(6, 13)]
        self.assertEqual(self.engine.score, 1)
        self.assertEqual(len(expected), len(result))
        self.assertListEqual(expected, result)

    def test_interact_with_double_length_food(self):
        level = os.path.join('.test_levels', 'double_length')
        self.engine = snake_engine.Driver(level, None)
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.check_food()
        result = self.move_and_get_snake_coords(7)
        expected = [Point(18, 13), Point(17, 13), Point(16, 13), Point(15, 13),
                    Point(14, 13), Point(13, 13), Point(12, 13), Point(11, 13),
                    Point(10, 13), Point(9, 13), Point(8, 13), Point(7, 13)]
        self.assertEqual(len(expected), len(result))
        self.assertListEqual(expected, result)

    def test_interact_with_reverse_food_to_left_side(self):
        level = os.path.join('.test_levels', 'reverse_to_left')
        self.engine = snake_engine.Driver(level, None)
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.check_food()
        result = self.move_and_get_snake_coords(1)
        expected = [Point(5, 13), Point(6, 13), Point(7, 13), Point(8, 13), Point(9, 13), Point(10, 13)]
        self.assertEqual(snake_components.Vector(-1, 0),
                         self.engine.snake.vector)
        self.assertListEqual(expected, result)

    def test_interact_with_reverse_food_to_right_side(self):
        level = os.path.join('.test_levels', 'reverse_to_right')
        self.engine = snake_engine.Driver(level, None)
        self.engine.snake.vector = snake_components.Vector(0, 1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        for i in range(6):
            self.engine.snake.move()
        self.engine.snake.check_food()
        result = self.move_and_get_snake_coords(2)
        expected = [Point(11, 14), Point(10, 14), Point(9, 14), Point(8, 14), Point(7, 14), Point(6, 14)]
        self.assertEqual(snake_components.Vector(1, 0),
                         self.engine.snake.vector)
        self.assertListEqual(expected, result)

    def test_interact_with_reverse_food_up(self):
        level = os.path.join('.test_levels', 'reverse_up')
        self.engine = snake_engine.Driver(level, None)
        self.engine.snake.vector = snake_components.Vector(0, 1)
        for i in range(7):
            self.engine.snake.move()
        self.engine.snake.check_food()
        result = self.move_and_get_snake_coords(2)
        expected = [Point(10, 13), Point(10, 14), Point(10, 15), Point(10, 16), Point(10, 17), Point(10, 18)]
        self.assertEqual(snake_components.Vector(0, -1),
                         self.engine.snake.vector)
        self.assertListEqual(expected, result)

    def test_interact_with_reverse_food_down(self):
        level = os.path.join('.test_levels', 'reverse_down')
        self.engine = snake_engine.Driver(level, None)
        self.engine.snake.vector = snake_components.Vector(0, -1)
        for i in range(7):
            self.engine.snake.move()
        self.engine.snake.check_food()
        result = self.move_and_get_snake_coords(2)
        expected = [Point(10, 13), Point(10, 12), Point(10, 11), Point(10, 10), Point(10, 9), Point(10, 8)]
        self.assertEqual(snake_components.Vector(0, 1),
                         self.engine.snake.vector)
        self.assertListEqual(expected, result)

    def test_interact_with_borders_in_levels_with_edges(self):
        level = os.path.join('.test_levels', 'teleport')
        self.engine = snake_engine.Driver(level, None)
        self.engine.snake.vector = snake_components.Vector(0, 1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        for i in range(11):
            self.engine.snake.move()
            self.engine.snake.check_walls()
        self.assertFalse(self.engine.in_game)
        self.assertEqual(0, self.engine.snake.hp)


class DriverActions(unittest.TestCase):

    def test_teleport_create(self):
        self.engine = snake_engine.Driver(1, None)
        self.assertTrue(type(self.engine.teleport.start) is Point)
        self.assertTrue(type(self.engine.teleport.end) is Point)

    def test_teleport_features(self):
        level = os.path.join('.test_levels', 'teleport')
        self.engine = snake_engine.Driver(level, None)
        self.assertTrue(
            Point(12, 13) in self.engine.obstacles['edges'] and Point(0, 19) in self.engine.obstacles['edges'])
        for i in range(3):
            self.engine.snake.move()

    def test_teleport_in_empty_map(self):
        level = os.path.join('.test_levels', 'empty_map')
        self.engine = snake_engine.Driver(level, None)
        self.engine.snake.vector = snake_components.Vector(1, 0)
        for i in range(2):
            self.engine.snake.move()
            self.engine.snake.check_walls()
        self.assertEqual(0, self.engine.snake.blocks[0].map_coords.x)
        self.assertEqual(13, self.engine.snake.blocks[0].map_coords.y)
        self.engine.snake.vector = snake_components.Vector(0, 1)
        for i in range(17):
            self.engine.snake.move()
            self.engine.snake.check_walls()
        self.assertEqual(0, self.engine.snake.blocks[0].map_coords.x)
        self.assertEqual(0, self.engine.snake.blocks[0].map_coords.y)
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(0, -1)
        self.engine.snake.move()
        self.engine.snake.check_walls()
        self.assertEqual(29, self.engine.snake.blocks[0].map_coords.y)
        self.assertEqual(1, self.engine.snake.blocks[0].map_coords.x)

    def test_restart_game(self):
        self.engine = snake_engine.Driver(1, None)
        self.engine.snake.vector = snake_components.Vector(0, -1)
        for i in range(9):
            self.engine.snake.move()
            self.engine.snake.check_walls()
        self.assertFalse(self.engine.in_game)
        self.engine.restart_the_game()
        snake_coords = []
        for block in self.engine.snake.blocks:
            snake_coords.append(block.map_coords)
        self.assertTrue(self.engine.in_game)
        self.assertIsNotNone(self.engine.food.type)
        self.assertIsNotNone(self.engine.food.map_coords)
        self.assertListEqual([Point(2, 14), Point(1, 14), Point(0, 14)], snake_coords)

    def test_create_level(self):
        self.engine = snake_engine.Driver(0, None)
        level_map = []
        for y in range(30):
            level_map.append([])
            for x in range(40):
                level_map[y].append(0)
        for y in range(30):
            for x in range(40):
                if y == 2 and (x == 1 or x == 2 or x == 3):
                    level_map[y][x] = 1
        self.assertListEqual(level_map, self.engine.map)

    def test_update_snake_state(self):
        self.engine = snake_engine.Driver(0, None)
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.update_snake_state()
        level_map = []
        for y in range(30):
            level_map.append([])
            for x in range(40):
                level_map[y].append(0)
        for y in range(30):
            for x in range(40):
                if y == 2 and (x == 2 or x == 3 or x == 4):
                    level_map[y][x] = 1
        self.assertListEqual(level_map, self.engine.map)


if __name__ == '__main__':
    unittest.main()

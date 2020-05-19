#!/usr/bin/env python3

import unittest
import snake_engine
import snake_components


class SnakeMove(unittest.TestCase):
    def setUp(self):
        self.engine = snake_engine.Driver(r'test_levels\move', None)

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
        expected = [(11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13)]
        self.assertEqual(expected, result)

    def test_move_up_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(0, -1)
        result = self.move_and_get_snake_coords(1)
        expected = [(10, 12), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13)]
        self.assertEqual(expected, result)

    def test_move_down_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        result = self.move_and_get_snake_coords(1)
        expected = [(10, 14), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13)]
        self.assertEqual(expected, result)

    def test_move_down_for_three_blocks(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        result = self.move_and_get_snake_coords(3)
        expected = [(10, 16), (10, 15), (10, 14), (10, 13), (9, 13), (8, 13)]
        self.assertEqual(expected, result)

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
        expected = [(12, 12), (12, 13), (11, 13), (11, 14), (10, 14), (10, 13)]
        self.assertEqual(expected, result)
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        result = self.move_and_get_snake_coords(4)
        expected = [(8, 12), (9, 12), (10, 12), (11, 12), (12, 12), (12, 13)]
        self.assertEqual(expected, result)

    def test_stop_when_crashing(self):
        self.engine.snake.vector = snake_components.Vector(0, -1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        result = self.move_and_get_snake_coords(11)
        expected = [(-1, 12), (0, 12), (1, 12), (2, 12), (3, 12), (4, 12)]
        self.engine.snake.check_walls()
        self.assertEqual(self.engine.in_game, False)
        self.assertEqual(expected, result)
        self.engine.snake.check_walls()
        self.engine.snake.move()
        self.assertEqual(expected, result)

    def test_self_eating(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(0, -1)
        result = self.move_and_get_snake_coords(1)
        expected = [(9, 13), (9, 14), (10, 14), (10, 13), (9, 13), (8, 13)]
        self.engine.snake.check_self_eating()
        self.assertEqual(self.engine.in_game, False)
        self.assertEqual(expected, result)
        self.engine.snake.move()
        self.assertEqual(expected, result)


class SnakeInteractionsWithMap(unittest.TestCase):

    def move_and_get_snake_coords(self, count):
        for i in range(count):
            self.engine.snake.move()
        coords = []
        for block in self.engine.snake.blocks:
            coords.append(block.map_coords)
        return coords

    def test_interact_with_default_food(self):
        self.engine = snake_engine.Driver(r'test_levels\default_food', None)
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.check_eat()
        result = self.move_and_get_snake_coords(1)
        expected = [(12, 13), (11, 13), (10, 13), (9, 13),
                    (8, 13), (7, 13), (6, 13)]
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    def test_interact_with_double_length_food(self):
        self.engine = snake_engine.Driver(r'test_levels\double_length', None)
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.check_eat()
        result = self.move_and_get_snake_coords(7)
        expected = [(18, 13), (17, 13), (16, 13), (15, 13),
                    (14, 13), (13, 13), (12, 13), (11, 13),
                    (10, 13), (9, 13), (8, 13), (7, 13)]
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    def test_interact_with_reverse_food_to_left_side(self):
        self.engine = snake_engine.Driver(r'test_levels\reverse_to_left', None)
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.check_eat()
        result = self.move_and_get_snake_coords(1)
        expected = [(5, 13), (6, 13), (7, 13), (8, 13), (9, 13), (10, 13)]
        self.assertEqual(snake_components.Vector(-1, 0),
                         self.engine.snake.vector)
        self.assertEqual(expected, result)

    def test_interact_with_reverse_food_to_right_side(self):
        self.engine = snake_engine.Driver(
            r'test_levels\reverse_to_right', None)
        self.engine.snake.vector = snake_components.Vector(0, 1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        for i in range(6):
            self.engine.snake.move()
        self.engine.snake.check_eat()
        result = self.move_and_get_snake_coords(2)
        expected = [(11, 14), (10, 14), (9, 14), (8, 14), (7, 14), (6, 14)]
        self.assertEqual(snake_components.Vector(1, 0),
                         self.engine.snake.vector)
        self.assertEqual(expected, result)

    def test_interact_with_reverse_food_up(self):
        self.engine = snake_engine.Driver(r'test_levels\reverse_up', None)
        self.engine.snake.vector = snake_components.Vector(0, 1)
        for i in range(7):
            self.engine.snake.move()
        self.engine.snake.check_eat()
        result = self.move_and_get_snake_coords(2)
        expected = [(10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (10, 18)]
        self.assertEqual(snake_components.Vector(0, -1),
                         self.engine.snake.vector)
        self.assertEqual(expected, result)

    def test_interact_with_reverse_food_down(self):
        self.engine = snake_engine.Driver(r'test_levels\reverse_down', None)
        self.engine.snake.vector = snake_components.Vector(0, -1)
        for i in range(7):
            self.engine.snake.move()
        self.engine.snake.check_eat()
        result = self.move_and_get_snake_coords(2)
        expected = [(10, 13), (10, 12), (10, 11), (10, 10), (10, 9), (10, 8)]
        self.assertEqual(snake_components.Vector(0, 1),
                         self.engine.snake.vector)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

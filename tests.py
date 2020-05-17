#!/usr/bin/env python3

import unittest
import snake_engine
import snake_components


class TestMove(unittest.TestCase):
    def setUp(self):
        self.engine = snake_engine.Driver(r'test_levels\move_only', True)

    def move_and_get_result(self, count):
        for i in range(count):
            self.engine.snake.move()
        coords = []
        for block in self.engine.snake.blocks:
            coords.append(block.map_coords)
        return coords

    def test_move_right_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(1, 0)
        result = self.move_and_get_result(1)
        expected = [(11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13)]
        self.assertEqual(expected, result)

    def test_move_up_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(0, -1)
        result = self.move_and_get_result(1)
        expected = [(10, 12), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13)]
        self.assertEqual(expected, result)

    def test_move_down_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        result = self.move_and_get_result(1)
        expected = [(10, 14), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13)]
        self.assertEqual(expected, result)

    def test_move_down_for_three_blocks(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        result = self.move_and_get_result(3)
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
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        result = self.move_and_get_result(4)
        expected = [(8, 12), (9, 12), (10, 12), (11, 12), (12, 12), (12, 13)]
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3

import unittest
import snake_engine
import snake_components
from config import WIDTH, HEIGHT, BLOCK_SIZE


class TestMove(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = snake_engine.Driver('test_level', True)

    def tearDown(self) -> None:
        pass

    def test_move_right_for_one_block(self):
        self.engine.snake.move()
        snake_coords_after_move = []
        for block in self.engine.snake.blocks:
            snake_coords_after_move.append(block.map_coords)
        self.assertEqual([(4, 1), (3, 1), (2, 1)], snake_coords_after_move)


if __name__ == '__main__':
    unittest.main()

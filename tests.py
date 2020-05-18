#!/usr/bin/env python3

import unittest
import snake_engine
import snake_components


class TestSnakeInteractionsWithMap(unittest.TestCase):
    def setUp(self):
        self.engine = snake_engine.Driver(r'test_levels\interactions', None)

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
        self.assertEqual(expected, result, "Snake don't moves to right side for one block")

    def test_move_up_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(0, -1)
        result = self.move_and_get_snake_coords(1)
        expected = [(10, 12), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13)]
        self.assertEqual(expected, result, "Snake don't moves up for one block")

    def test_move_down_for_one_block(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        result = self.move_and_get_snake_coords(1)
        expected = [(10, 14), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13)]
        self.assertEqual(expected, result, "Snake don't moves down for one block")

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
        self.assertEqual(expected, result, "Snake moves wrong for not straight way")

    def test_stop_when_crashing(self):
        self.engine.snake.vector = snake_components.Vector(0, -1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        result = self.move_and_get_snake_coords(11)
        expected = [(-1, 12), (0, 12), (1, 12), (2, 12), (3, 12), (4, 12)]
        self.engine.snake.check_walls()
        self.assertEqual(self.engine.in_game, False, "Game isn't over")
        self.assertEqual(expected, result, "Snake didn't get out of map")
        self.engine.snake.check_walls()
        self.engine.snake.move()
        self.assertEqual(expected, result, "Snake is moving but game is over")

    def test_interact_with_default_food(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        for i in range(3):
            self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(1, 0)
        self.engine.snake.move()
        self.engine.snake.check_eat()
        result = self.move_and_get_snake_coords(1)
        expected = [(12, 16), (11, 16), (10, 16), (10, 15), (10, 14), (10, 13), (9, 13)]
        self.assertEqual(len(expected), len(result), "Snake ate food but didn't grow up")
        self.assertEqual(expected, result, "Snake grow up, but for something went wrong with her blocks position")

    def test_interact_with_double_length_food(self):

        self.engine.snake.vector = snake_components.Vector(1, 0)
        for i in range(8):
            self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(0, -1)
        for i in range(2):
            self.engine.snake.move()
        print(self.engine.snake.blocks[0].map_coords)
        for row in self.engine.map:
            for x in row:
                print("{:4d}".format(x), end="")
            print()

        print('\n')
        self.engine.snake.check_eat()
        result = self.move_and_get_snake_coords(7)

        expected = [(18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (18, 10), (18, 11), (18, 12), (18, 13), (17, 13), (16, 13), (15, 13)]
        self.assertEqual(len(expected), len(result), "Snake ate food but didn't grow up 2 times")

    def test_self_eating(self):
        self.engine.snake.vector = snake_components.Vector(0, 1)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(-1, 0)
        self.engine.snake.move()
        self.engine.snake.vector = snake_components.Vector(0, -1)
        result = self.move_and_get_snake_coords(1)
        expected = [(9, 13), (9, 14), (10, 14), (10, 13), (9, 13), (8, 13)]
        self.engine.snake.check_self_eating()
        self.assertEqual(self.engine.in_game, False, "Game isn't over")
        self.assertEqual(expected, result, "Snake moves wrong for not straight way")
        self.engine.snake.move()
        self.assertEqual(expected, result, "Snake is moving but game is over")


if __name__ == '__main__':
    unittest.main()

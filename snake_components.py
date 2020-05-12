#!/usr/bin/env python3

import time
import random
from config import (DEFAULT_FOOD_PROBABILITY,
                    DOUBLE_LENGTH_PROBABILITY,
                    BOOST_PROBABILITY,
                    BOOST_COEFFICIENT,
                    REVERSE_PROBABILITY)


class Vector:
    """Компонент «вектор змейки»"""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block:
    """Компонент «блок змейки»"""

    def __init__(self, x, y):
        self.map_coords = (x, y)


class Food:
    """Компонент «еда змейки»"""

    def __init__(self):
        self.map_coords = None
        self.type = None


class Snake:
    """Компонент «змейка»"""

    def __init__(self, blocks, driver):
        self.driver = driver
        self.blocks = blocks
        self.vector = Vector(1, 0)
        self.last_handled_vector = Vector(1, 0)

    def move(self):
        """Движение змейки"""
        if self.driver.in_game:
            for y in range(len(self.driver.map)):
                for x in range(len(self.driver.map[y])):
                    for block in self.driver.snake.blocks:
                        if (x, y) == block.map_coords:
                            self.driver.map[y][x] = 0

            self.last_handled_vector = self.vector
            for index in reversed(range(1, len(self.blocks))):
                x, y = self.blocks[index - 1].map_coords
                self.blocks[index].map_coords = (x, y)

            x, y = self.blocks[0].map_coords
            self.blocks[0].map_coords = (x + self.vector.x,
                                         y + self.vector.y)
            self.driver.update_snake_state()

    def check_obstacles(self):
        """Проверка встречи всевозможных препятствий при движении"""

        self.check_self_eating()
        self.check_eat()
        self.check_walls()

    def check_self_eating(self):
        """Проверка столкновения змейки с самой собой"""

        for i in range(2, len(self.blocks)):
            if self.blocks[0].map_coords == self.blocks[i].map_coords:
                self.driver.in_game = False

    def check_eat(self):
        """Обработка встречи еды"""

        if (self.blocks[0].map_coords ==
                self.driver.food.map_coords):
            if self.driver.food.type == 5:
                self.blocks.append(
                    Block(self.blocks[-1].map_coords[0], self.blocks[-1].map_coords[1]))
                self.driver.update_score(1)
            if self.driver.food.type == 6:
                for i in range(len(self.blocks)):
                    self.blocks.append(
                        Block(self.blocks[-1].map_coords[0], self.blocks[-1].map_coords[1]))
                self.driver.update_score(self.driver.score)
            if self.driver.food.type == 7:
                self.driver.update_score(2)
                self.driver.current_update_freq /= BOOST_COEFFICIENT
                self.driver.boost_start_moment = time.perf_counter()
            if self.driver.food.type == 8:
                if (self.blocks[-1].map_coords[0] == self.blocks[-2].map_coords[0] and
                        self.blocks[-2].map_coords[1] == self.blocks[-1].map_coords[1] - 1):
                    self.vector.y = 1
                    self.vector.x = 0
                elif (self.blocks[-1].map_coords[0] == self.blocks[-2].map_coords[0] and
                      self.blocks[-2].map_coords[1] == self.blocks[-1].map_coords[1] + 1):
                    self.vector.y = -1
                    self.vector.x = 0
                elif (self.blocks[-1].map_coords[1] == self.blocks[-2].map_coords[1] and
                      self.blocks[-1].map_coords[0] == self.blocks[-2].map_coords[0] - 1):
                    self.vector.y = 0
                    self.vector.x = -1
                elif (self.blocks[-1].map_coords[1] == self.blocks[-2].map_coords[1] and
                      self.blocks[-1].map_coords[0] == self.blocks[-2].map_coords[0] + 1):
                    self.vector.y = 0
                    self.vector.x = 1
                self.blocks.reverse()
                self.driver.update_score(2)
            if self.driver.vanilla:
                self.driver.get_food([5])
            else:
                self.driver.get_food(random.choices(
                    list(self.driver.food_types.keys()),
                    weights=[DEFAULT_FOOD_PROBABILITY,
                             DOUBLE_LENGTH_PROBABILITY,
                             BOOST_PROBABILITY,
                             REVERSE_PROBABILITY]))

    def check_walls(self):
        """Проверка на столкновение змейки со стеной"""
        if (self.blocks[0].map_coords[0] > 39 or
                self.blocks[0].map_coords[0] < 0 or
                self.blocks[0].map_coords[1] > 29 or
                self.blocks[0].map_coords[1] < 0):
            self.driver.in_game = False
        if self.driver.level != 0:
            for obstacle in self.driver.walls_coords:
                if self.driver.snake.blocks[0].map_coords == obstacle:
                    self.driver.in_game = False

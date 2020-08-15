#!/usr/bin/env python3

import time
import random
from config import (DEFAULT_FOOD_PROBABILITY,
                    DOUBLE_LENGTH_PROBABILITY,
                    BOOST_PROBABILITY,
                    BOOST_COEFFICIENT,
                    REVERSE_PROBABILITY)

class Teleport:
    def __init__(self, driver):
        edges = driver.obstacles['edges']
        start_end_indexes = random.sample(range(0, len(edges) - 1), 2)
        self.start = Point(edges[start_end_indexes[0]].x,
                           edges[start_end_indexes[0]].y)
        self.end = Point(edges[start_end_indexes[1]].x,
                         edges[start_end_indexes[1]].y)
        driver.map[self.start.y][self.start.x] = 2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Vector:
    """Компонент «вектор змейки»"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Block:
    """Компонент «блок змейки»"""

    def __init__(self, x, y):
        self.map_coords = Point(x, y)


class Food:
    """Компонент «еда змейки»"""

    def __init__(self):
        self.map_coords = None
        self.type = None


class Snake:
    """Компонент «змейка»"""

    def __init__(self, blocks, driver):
        self.hp = 3
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
                        if Point(x, y) == block.map_coords:
                            self.driver.map[y][x] = 0

            self.last_handled_vector = self.vector
            for index in reversed(range(1, len(self.blocks))):
                self.blocks[index].map_coords = Point(
                    self.blocks[index - 1].map_coords.x,
                    self.blocks[index - 1].map_coords.y)
            x = self.blocks[0].map_coords.x
            y = self.blocks[0].map_coords.y
            self.blocks[0].map_coords = Point(x + self.vector.x,
                                              y + self.vector.y)

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
                    Block(self.blocks[-1].map_coords.x,
                          self.blocks[-1].map_coords.y))
                self.driver.update_score(1)
            elif self.driver.food.type == 6:
                for i in range(len(self.blocks)):
                    self.blocks.append(
                        Block(self.blocks[-1].map_coords.x,
                              self.blocks[-1].map_coords.y))
                self.driver.update_score(self.driver.score)
            elif self.driver.food.type == 7:
                self.driver.update_score(2)
                self.driver.current_update_freq /= BOOST_COEFFICIENT
                self.driver.boost_start_moment = time.perf_counter()
            elif self.driver.food.type == 8:
                if (self.blocks[-1].map_coords.x ==
                        self.blocks[-2].map_coords.x and
                        self.blocks[-2].map_coords.y ==
                        self.blocks[-1].map_coords.y - 1):
                    self.vector.y = 1
                    self.vector.x = 0
                if (self.blocks[-1].map_coords.x ==
                        self.blocks[-2].map_coords.x and
                        self.blocks[-2].map_coords.y ==
                        self.blocks[-1].map_coords.y + 1):
                    self.vector.y = -1
                    self.vector.x = 0
                if (self.blocks[-1].map_coords.y ==
                        self.blocks[-2].map_coords.y and
                        self.blocks[-1].map_coords.x ==
                        self.blocks[-2].map_coords.x - 1):
                    self.vector.y = 0
                    self.vector.x = -1
                if (self.blocks[-1].map_coords.y ==
                        self.blocks[-2].map_coords.y and
                        self.blocks[-1].map_coords.x ==
                        self.blocks[-2].map_coords.x + 1):
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

        if self.driver.in_game:
            if int(self.driver.level) == 0:
                if self.blocks[0].map_coords.x > 39:
                    self.blocks[0].map_coords =\
                        Point(0, self.blocks[0].map_coords.y)
                if self.blocks[0].map_coords.x < 0:
                    self.blocks[0].map_coords =\
                        Point(39, self.blocks[0].map_coords.y)
                if self.blocks[0].map_coords.y > 29:
                    self.blocks[0].map_coords =\
                        Point(self.blocks[0].map_coords.x, 0)
                if self.blocks[0].map_coords.y < 0:
                    self.blocks[0].map_coords =\
                        Point(self.blocks[0].map_coords.x, 29)
            else:
                teleport = self.driver.teleport
                if self.blocks[0].map_coords == Point(
                        teleport.start.x, teleport.start.y):
                    self.driver.map[teleport.start.y][teleport.start.x] = 9
                    if self.driver.map[teleport.end.y][teleport.end.x + 1] == 0:
                        self.blocks[0].map_coords =\
                            Point(teleport.end.x + 1, teleport.end.y)
                        self.driver.snake.vector = Vector(1, 0)
                    elif self.driver.map[teleport.end.y][teleport.end.x - 1] == 0:
                        self.blocks[0].map_coords =\
                            Point(teleport.end.x - 1, teleport.end.y)
                        self.driver.snake.vector = Vector(-1, 0)
                    elif self.driver.map[teleport.end.y + 1][teleport.end.x] == 0:
                        self.blocks[0].map_coords =\
                            Point(teleport.end.x, teleport.end.y + 1)
                        self.driver.snake.vector = Vector(0, 1)
                    elif self.driver.map[teleport.end.y - 1][teleport.end.x] == 0:
                        self.blocks[0].map_coords =\
                            Point(teleport.end.x, teleport.end.y - 1)
                        self.driver.snake.vector = Vector(0, -1)
                    self.driver.teleport = Teleport(self.driver)
                if (self.blocks[0].map_coords.x > 39 or
                        self.blocks[0].map_coords.x < 0 or
                        self.blocks[0].map_coords.y > 29 or
                        self.blocks[0].map_coords.y < 0):
                    self.driver.in_game = False
        if self.driver.level != 0 and self.hp > 0:
            for obstacle in self.driver.obstacles['walls']:
                if self.driver.snake.blocks[0].map_coords == obstacle:
                    self.hp -= 1
                    if self.hp == 0:
                        self.driver.in_game = False

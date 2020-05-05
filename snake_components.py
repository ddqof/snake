#!/usr/bin/env python3

import time
import random
from config import (WIDTH, HEIGHT, BLOCK_SIZE,
                    DEFAULT_FOOD_PROBABILITY,
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

    def __init__(self, x, y, canvas):
        self.image = canvas.create_rectangle(x, y,
                                             x + BLOCK_SIZE, y + BLOCK_SIZE,
                                             fill='white')


class Snake:
    """Компонент «змейка»"""

    def __init__(self, blocks, driver):
        self.blocks = blocks
        self.driver = driver
        self.vector = Vector(1, 0)
        self.last_handled_vector = Vector(1, 0)

    def move(self):
        """Движение змейки"""

        self.last_handled_vector = self.vector
        for index in reversed(range(1, len(self.blocks))):
            block = self.blocks[index].image
            x1, y1, x2, y2 = self.driver.coords(self.blocks[index - 1].image)
            self.driver.coords(block, x1, y1, x2, y2)

        x1, y1, x2, y2 = self.driver.coords(self.blocks[0].image)
        self.driver.coords(self.blocks[0].image,
                           x1 + self.vector.x * BLOCK_SIZE,
                           y1 + self.vector.y * BLOCK_SIZE,
                           x2 + self.vector.x * BLOCK_SIZE,
                           y2 + self.vector.y * BLOCK_SIZE)
        self.check_obstacles()

    def check_obstacles(self):
        """Проверка встречи всевозможных препятствий при движении"""

        self.check_self_eating()
        if self.driver.in_game:
            self.check_eat()
            self.check_walls()

    def check_self_eating(self):
        """Проверка столкновения змейки с самой собой"""

        for i in range(2, len(self.blocks)):
            if (self.driver.coords(self.blocks[0].image) ==
                    self.driver.coords(self.blocks[i].image)):
                self.driver.finish_the_game()

    def check_eat(self):
        """Обработка встречи еды"""

        if (self.driver.coords(self.blocks[0].image) ==
                self.driver.coords(self.driver.food.image)):
            self.driver.delete(self.driver.food.image)
            if self.driver.food.type == 'red':
                self.blocks.append(
                    Block(self.driver.coords(self.blocks[-1].image)[0],
                          self.driver.coords(self.blocks[-1].image)[1],
                          self.driver))
                self.driver.update_score(1)
            if self.driver.food.type == 'green':
                for i in range(len(self.blocks)):
                    self.blocks.append(
                        Block(self.driver.coords(self.blocks[-1].image)[0],
                              self.driver.coords(self.blocks[-1].image)[1],
                              self.driver))
                self.driver.update_score(self.driver.score)
            if self.driver.food.type == 'cyan':
                self.driver.update_score(1)
                self.driver.current_update_freq /= BOOST_COEFFICIENT
                self.driver.start_speed_up_time = time.perf_counter()
            if self.driver.food.type == 'purple':
                if (self.driver.coords(self.blocks[-1].image)[0] ==
                        self.driver.coords(self.blocks[-2].image)[0] and
                        self.driver.coords(self.blocks[-2].image)[1] ==
                        self.driver.coords(self.blocks[-1].image)[1] - BLOCK_SIZE):
                    self.vector.y = 1
                    self.vector.x = 0
                elif (self.driver.coords(self.blocks[-1].image)[0] ==
                      self.driver.coords(self.blocks[-2].image)[0] and
                      self.driver.coords(self.blocks[-2].image)[1] ==
                      self.driver.coords(self.blocks[-1].image)[1] + BLOCK_SIZE):
                    self.vector.y = -1
                    self.vector.x = 0
                elif (self.driver.coords(self.blocks[-1].image)[1] ==
                      self.driver.coords(self.blocks[-2].image)[1] and
                      self.driver.coords(self.blocks[-1].image)[0] ==
                      self.driver.coords(self.blocks[-2].image)[0] - BLOCK_SIZE):
                    self.vector.y = 0
                    self.vector.x = -1
                elif (self.driver.coords(self.blocks[-1].image)[1] ==
                      self.driver.coords(self.blocks[-2].image)[1] and
                      self.driver.coords(self.blocks[-1].image)[0] ==
                      self.driver.coords(self.blocks[-2].image)[0] + BLOCK_SIZE):
                    self.vector.y = 0
                    self.vector.x = 1
                self.blocks.reverse()
                self.driver.update_score(2)
            if self.driver.vanilla:
                self.driver.create_food(['red'])
            else:
                self.driver.create_food(random.choices(
                    list(self.driver.food_types.values()),
                    weights=[DEFAULT_FOOD_PROBABILITY,
                             DOUBLE_LENGTH_PROBABILITY,
                             BOOST_PROBABILITY,
                             REVERSE_PROBABILITY]))

    def check_walls(self):
        """Проверка на столкновение змейки со стеной"""

        if (self.driver.coords(self.blocks[0].image)[2] > WIDTH or
                self.driver.coords(self.blocks[0].image)[0] < 0 or
                self.driver.coords(self.blocks[0].image)[3] > HEIGHT or
                self.driver.coords(self.blocks[0].image)[1] < 0):
            self.driver.finish_the_game()

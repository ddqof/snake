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

    def __init__(self, blocks, canvas):
        self.blocks = blocks
        self.master = canvas
        self.vector = Vector(1, 0)
        self.last_vector = Vector(1, 0)

    def move(self):
        """Движение змейки"""

        self.last_vector = self.vector
        for index in reversed(range(1, len(self.blocks))):
            block = self.blocks[index].image
            x1, y1, x2, y2 = self.master.coords(self.blocks[index - 1].image)
            self.master.coords(block, x1, y1, x2, y2)

        x1, y1, x2, y2 = self.master.coords(self.blocks[0].image)
        self.master.coords(self.blocks[0].image,
                           x1 + self.vector.x * BLOCK_SIZE,
                           y1 + self.vector.y * BLOCK_SIZE,
                           x2 + self.vector.x * BLOCK_SIZE,
                           y2 + self.vector.y * BLOCK_SIZE)
        self.check_obstacles()

    def check_obstacles(self):
        """Проверка встречи всевозможных препятствий при движении"""

        self.check_self_eating()
        if self.master.in_game:
            self.check_eat()
            self.check_walls()

    def check_self_eating(self):
        """Проверка столкновения змейки с самой собой"""

        for i in range(2, len(self.blocks)):
            if (self.master.coords(self.blocks[0].image) ==
                    self.master.coords(self.blocks[i].image)):
                self.master.finish_the_game()

    def check_eat(self):
        """Обработка встречи еды"""

        if (self.master.coords(self.blocks[0].image) ==
                self.master.coords(self.master.food.image)):
            self.master.delete(self.master.food.image)
            if self.master.food.type == 'red':
                self.blocks.append(
                    Block(self.master.coords(self.blocks[-1].image)[0],
                          self.master.coords(self.blocks[-1].image)[1],
                          self.master))
                self.master.update_score(1)
            if self.master.food.type == 'green':
                for i in range(len(self.blocks)):
                    self.blocks.append(
                        Block(self.master.coords(self.blocks[-1].image)[0],
                              self.master.coords(self.blocks[-1].image)[1],
                              self.master))
                self.master.update_score(self.master.score)
            if self.master.food.type == 'cyan':
                self.master.update_score(1)
                self.master.current_update_freq /= BOOST_COEFFICIENT
                self.master.start_speed_up_time = time.perf_counter()
            if self.master.food.type == 'purple':
                self.blocks.reverse()
                # if self.vector.x == 0:
                #     self.vector.y *= -1
                # if self.vector.y == 0:
                #     self.vector.x *= -1
                self.master.update_score(2)
            if self.master.vanilla:
                self.master.create_food(['red'])
            else:
                self.master.create_food(random.choices(
                    list(self.master.food_types.values()),
                    weights=[DEFAULT_FOOD_PROBABILITY,
                             DOUBLE_LENGTH_PROBABILITY,
                             BOOST_PROBABILITY,
                             REVERSE_PROBABILITY]))

    def check_walls(self):
        """Проверка на столкновение змейки со стеной"""

        if (self.master.coords(self.blocks[0].image)[2] > WIDTH or
                self.master.coords(self.blocks[0].image)[0] < 0 or
                self.master.coords(self.blocks[0].image)[3] > HEIGHT or
                self.master.coords(self.blocks[0].image)[1] < 0):
            self.master.finish_the_game()

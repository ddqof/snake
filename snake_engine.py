#!/usr/bin/env python3

import time
import snake_components
import random
import os
from config import (SNAKE_SPEED, BLOCK_SIZE, WIDTH, HEIGHT,
                    DEFAULT_FOOD_PROBABILITY,
                    DOUBLE_LENGTH_PROBABILITY,
                    BOOST_PROBABILITY,
                    REVERSE_PROBABILITY)


class Driver:
    """Компонент «контроллер игры»"""

    def __init__(self, lvl, food_flag):
        self.vanilla = food_flag
        self.map = []
        for y in range(int(BLOCK_SIZE * (HEIGHT / BLOCK_SIZE ** 2))):
            self.map.append([])
            for x in range(int(BLOCK_SIZE * (WIDTH / BLOCK_SIZE ** 2))):
                self.map[y].append(0)
        self.default_update_freq = int(1 / SNAKE_SPEED * 1000)
        self.current_update_freq = self.default_update_freq
        self.boost_start_moment = 0
        self.level = int(lvl)
        self.in_game = None
        self.food = snake_components.Food()
        self.obstacles = self.create_level()
        if self.level != 0:
            self.create_teleport()
        self.obstacles['snake_blocks'].reverse()
        self.snake = snake_components.Snake(
            self.obstacles['snake_blocks'], self)
        self.food_types = {5: 'red', 6: 'green', 7: 'cyan', 8: 'purple'}
        if self.vanilla:
            self.get_food([5])
        if self.vanilla is False:
            self.get_food(random.choices((list(self.food_types.keys())),
                                         weights=[DEFAULT_FOOD_PROBABILITY,
                                                  DOUBLE_LENGTH_PROBABILITY,
                                                  BOOST_PROBABILITY,
                                                  REVERSE_PROBABILITY]))
        self.score = 0
        self.high_score = 0

    def get_food(self, food_type):
        """Создание еды для змейки"""

        block_coords = {}
        food_x = random.randint(1, BLOCK_SIZE * (WIDTH / BLOCK_SIZE ** 2) - 2)
        food_y = random.randint(1, BLOCK_SIZE * (HEIGHT / BLOCK_SIZE ** 2) - 2)
        food_coords = (food_x, food_y)
        index = 0
        for block in self.snake.blocks:
            block_coords[index] = block.map_coords
            index += 1
        for lvl_block in self.obstacles['walls']:
            block_coords[index] = lvl_block
            index += 1
        if food_coords not in block_coords.values():
            self.food.map_coords = food_coords
            self.food.type = food_type[0]
            self.map[food_y][food_x] = food_type[0]
        else:
            self.get_food(food_type)

    def check_boost_time(self):
        """Проверка истечения времени для ускорения"""

        if self.boost_start_moment != 0:
            if int(time.perf_counter() - self.boost_start_moment) == 3:
                self.current_update_freq = self.default_update_freq

    def create_level(self):
        """Создание игрового уровня"""

        obstacles = {'walls': [], 'edges': [], 'snake_blocks': []}
        try:
            level = os.path.join('levels', str(self.level) + '.txt')
            with open(level, 'r') as f:
                x = 0
                y = 0
                for line in f:
                    for symbol in line:
                        if (symbol == '5' or symbol == '6' or
                                symbol == '7' or symbol == '8'):
                            self.map[y][x] = int(symbol)
                            self.food.map_coords = (x, y)
                            self.food.type = int(symbol)
                        elif symbol == '9':
                            if (x != 0 and self.map[y][x - 1] == 0) or (y != 0 and self.map[y - 1][x] == 0):
                                obstacles['edges'].append((x, y))
                            self.map[y][x] = 9
                            obstacles['walls'].append((x, y))
                        elif symbol == '0':
                            if y != 0 and self.map[y - 1][x] == 9 and (x, y - 1) not in obstacles['edges']:
                                obstacles['edges'].append((x, y - 1))
                            if x != 0 and self.map[y][x - 1] == 9 and (x - 1, y) not in obstacles['edges']:
                                obstacles['edges'].append((x - 1, y))
                        elif symbol == '1':
                            self.map[y][x] = 1
                            obstacles['snake_blocks'].append(
                                snake_components.Block(x, y))
                        x += 1
                    y += 1
                    x = 0
            self.in_game = True
        except FileNotFoundError or TypeError:
            self.in_game = False
        return obstacles

    def create_teleport(self):
        edge_number = random.randint(0, len(self.obstacles['edges']))
        x = self.obstacles['edges'][edge_number][0]
        y = self.obstacles['edges'][edge_number][1]
        self.map[y][x] = 2

    def restart_the_game(self):
        """Перезапуск игры"""

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.map[y][x] = 0
        self.boost_start_moment = 0
        self.current_update_freq = self.default_update_freq
        self.score = 0
        self.obstacles = self.create_level()
        self.obstacles['snake_blocks'].reverse()
        self.snake = snake_components.Snake(
            self.obstacles['snake_blocks'], self)
        self.update_snake_state()
        for wall in self.obstacles['walls']:
            self.map[wall[1]][wall[0]] = 9
        if self.vanilla:
            self.get_food([5])
        else:
            self.get_food(random.choices(list(self.food_types.keys()),
                                         weights=[DEFAULT_FOOD_PROBABILITY,
                                                  DOUBLE_LENGTH_PROBABILITY,
                                                  BOOST_PROBABILITY,
                                                  REVERSE_PROBABILITY]))

        if self.level != 0:
            self.create_teleport()
        self.in_game = True

    def update_snake_state(self):
        """Обновление состояния змейки на игровом поле"""

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                for block in self.snake.blocks:
                    if (x, y) == block.map_coords:
                        self.map[y][x] = 1
        # for row in self.map:
        #     for elem in row:
        #         print(elem, end=' ')
        #     print()
        # print()

    def update_score(self, score):
        """Обновление игровых очков"""

        self.score = self.score + score
        if self.score > self.high_score:
            self.high_score = self.high_score + score

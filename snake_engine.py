#!/usr/bin/env python3

import time
import snake_components
import random
from config import (SNAKE_SPEED, BLOCK_SIZE, WIDTH, HEIGHT,
                    DEFAULT_FOOD_PROBABILITY,
                    DOUBLE_LENGTH_PROBABILITY,
                    BOOST_PROBABILITY,
                    REVERSE_PROBABILITY)


# TODO: добавить уровни

class Driver:
    """Компонент «контроллер игры»"""

    def __init__(self, lvl, vanilla_flag):
        self.vanilla = vanilla_flag
        self.snake = snake_components.Snake([
            snake_components.Block(3, 1),
            snake_components.Block(2, 1),
            snake_components.Block(1, 1)], self)
        self.map = []
        for y in range(int(BLOCK_SIZE * (HEIGHT / BLOCK_SIZE ** 2))):
            self.map.append([])
            for x in range(int(BLOCK_SIZE * (WIDTH / BLOCK_SIZE ** 2))):
                self.map[y].append(0)
        self.default_update_freq = int(1 / SNAKE_SPEED * 1000)
        self.current_update_freq = self.default_update_freq
        self.vector = snake_components.Vector(1, 0)
        self.boost_start_moment = 0
        self.food = snake_components.Food()
        self.food_types = {5: 'red', 6: 'green', 7: 'cyan', 8: 'purple'}
        if self.vanilla:
            self.get_food([5])
        else:
            self.get_food(random.choices((list(self.food_types.keys())),
                                         weights=[DEFAULT_FOOD_PROBABILITY,
                                                  DOUBLE_LENGTH_PROBABILITY,
                                                  BOOST_PROBABILITY,
                                                  REVERSE_PROBABILITY]))
        self.level = lvl
        self.walls_coords = self.create_level(lvl)
        self.score = 0
        self.high_score = 0
        self.in_game = True
        self.last_handled_vector = snake_components.Vector(1, 0)

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
        # for lvl_block in self.level_walls:
        #     block_coords[index] = tuple(self.coords(lvl_block))
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

    def create_random_wall(self):
        """Создание еды для змейки"""

        walls = []
        walls_count = 0
        while walls_count < 50:
            block_coords = {}
            wall_x = random.randint(0, BLOCK_SIZE * (WIDTH / BLOCK_SIZE ** 2) - 1)
            wall_y = random.randint(0, BLOCK_SIZE * (HEIGHT / BLOCK_SIZE ** 2) - 1)
            index = 0
            for block in self.snake.blocks:
                block_coords[index] = block.map_coords
                index += 1
            block_coords[index] = self.food.map_coords
            if (wall_x, wall_y) not in block_coords.values():
                walls.append((wall_x, wall_y))
                self.map[wall_y][wall_x] = 9
                walls_count += 1

        return walls

    def create_level(self, lvl):
        walls = []
        # if lvl == 1:
        #     for i in range(40):
        #         walls.append(self.create_rectangle(BLOCK_SIZE * i, 0, BLOCK_SIZE * (i + 1), BLOCK_SIZE, fill='gray'))
        if lvl == 3:
            walls = self.create_random_wall()
        return walls

    def restart_the_game(self):
        """Перезаупуск игры"""

        for y in range(int(BLOCK_SIZE * (HEIGHT / BLOCK_SIZE ** 2))):
            for x in range(int(BLOCK_SIZE * (WIDTH / BLOCK_SIZE ** 2))):
                self.map[y][x] = 0
        self.boost_start_moment = 0
        self.current_update_freq = self.default_update_freq
        self.score = 0
        self.snake.blocks = [
            snake_components.Block(3, 1),
            snake_components.Block(2, 1),
            snake_components.Block(1, 1)]
        self.snake = snake_components.Snake(self.snake.blocks, self)
        self.update_snake_state()
        if self.vanilla:
            self.get_food([5])
        else:
            self.get_food(random.choices(list(self.food_types.keys()),
                                         weights=[DEFAULT_FOOD_PROBABILITY,
                                                  DOUBLE_LENGTH_PROBABILITY,
                                                  BOOST_PROBABILITY,
                                                  REVERSE_PROBABILITY]))
        self.walls_coords = self.create_level(self.level)
        self.in_game = True

    def update_snake_state(self):
        """Обновление состояния игрового поля"""

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                for block in self.snake.blocks:
                    if (x, y) == block.map_coords:
                        self.map[y][x] = 1

    def update_score(self, score):
        """Обновление игровых очков"""

        self.score = self.score + score
        if self.score > self.high_score:
            self.high_score = self.high_score + score

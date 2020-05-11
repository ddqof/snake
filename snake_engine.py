#!/usr/bin/env python3

import snake_components
import random
from config import (SNAKE_SPEED, BLOCK_SIZE, WIDTH, HEIGHT,
                    DEFAULT_FOOD_PROBABILITY,
                    DOUBLE_LENGTH_PROBABILITY,
                    BOOST_PROBABILITY,
                    REVERSE_PROBABILITY)


# TODO: добавить уровни

class Driver:
    """Компонент «двигатель игры»"""

    def __init__(self, lvl, vanilla_flag):
        self.vanilla = vanilla_flag
        self.snake = snake_components.Snake([
            snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE),
            snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE),
            snake_components.Block(BLOCK_SIZE, BLOCK_SIZE)], self)
        self.default_update_freq = int(1 / SNAKE_SPEED * 1000)
        self.current_update_freq = self.default_update_freq
        self.vector = snake_components.Vector(1, 0)
        # self.start_speed_up_time = 0
        # self.level_walls = []
        self.food = snake_components.Food()
        self.food_types = {0: 'red', 1: 'green', 2: 'cyan', 3: 'purple'}
        # self.level_walls = self.create_level(lvl)
        if self.vanilla:
            self.get_food(['red'])
        else:
            self.get_food(random.choices((list(self.food_types.values())),
                                         weights=[DEFAULT_FOOD_PROBABILITY,
                                                  DOUBLE_LENGTH_PROBABILITY,
                                                  BOOST_PROBABILITY,
                                                  REVERSE_PROBABILITY]))
        self.map = []
        self.init_map()
        self.score = 0
        self.high_score = 0
        self.in_game = True
        self.last_handled_vector = snake_components.Vector(1, 0)

    def init_map(self):
        for y in range(int(BLOCK_SIZE * (HEIGHT / BLOCK_SIZE ** 2))):
            self.map.append([])
            for x in range(int(BLOCK_SIZE * (WIDTH / BLOCK_SIZE ** 2))):
                self.map[y].append(0)

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                for block in self.snake.blocks:
                    if (x, y) == block.map_coords:
                        self.map[y][x] = 1

        for row in self.map:
            for x in row:
                print("{:4d}".format(x), end="")
            print()

    def get_food(self, food_colour):
        """Создание еды для змейки"""

        block_coords = {}
        food_x1 = BLOCK_SIZE * random.randint(
            1, BLOCK_SIZE * (WIDTH / BLOCK_SIZE ** 2) - 2)
        food_y1 = BLOCK_SIZE * random.randint(
            1, BLOCK_SIZE * (HEIGHT / BLOCK_SIZE ** 2) - 2)
        food_x2 = food_x1 + BLOCK_SIZE
        food_y2 = food_y1 + BLOCK_SIZE
        food = (food_x1, food_y1, food_x2, food_y2)
        index = 0
        for block in self.snake.blocks:
            block_coords[index] = block.canvas_coords
            index += 1
        # for lvl_block in self.level_walls:
        #     block_coords[index] = tuple(self.coords(lvl_block))
        if food not in block_coords.values():
            self.food.type = food_colour[0]
            self.food.canvas_coords = (food[0], food[1], food[2], food[3])
            self.food.map_coords = (food[0] / BLOCK_SIZE, food[1] / BLOCK_SIZE)
        else:
            self.get_food(food_colour)

    # def create_random_wall(self):
    #     """Создание еды для змейки"""
    #
    #     walls_count = 0
    #     level_walls_coords = []
    #     while walls_count < 50:
    #         block_coords = {}
    #         wall_x1 = BLOCK_SIZE * random.randint(
    #             1, BLOCK_SIZE * (WIDTH / BLOCK_SIZE ** 2) - 2)
    #         wall_y1 = BLOCK_SIZE * random.randint(
    #             1, BLOCK_SIZE * (HEIGHT / BLOCK_SIZE ** 2) - 2)
    #         wall_x2 = wall_x1 + BLOCK_SIZE
    #         wall_y2 = wall_y1 + BLOCK_SIZE
    #         wall = (wall_x1, wall_y1, wall_x2, wall_y2)
    #         for index in range(len(self.blocks)):
    #             block_coords[index] = tuple(self.coords(self.blocks[index].image))
    #         block_coords[len(self.blocks)] = tuple(self.coords(self.food))
    #         if wall not in block_coords.values():
    #             level_walls_coords.append(self.create_rectangle(
    #                 wall[0], wall[1], wall[2], wall[3], fill='grey'))
    #             walls_count += 1
    #     return level_walls_coords

    # def create_level(self, lvl):
    #     walls = []
    #     if lvl == 1:
    #         for i in range(40):
    #             walls.append(self.create_rectangle(BLOCK_SIZE * i, 0, BLOCK_SIZE * (i + 1), BLOCK_SIZE, fill='gray'))
    #     if lvl == 2:
    #         walls = self.create_random_wall()
    #     return walls

    # def finish_the_game(self):
    #     """Остановка и завершение игры"""
    #
    #     self.in_game = False
    #     self.create_text(
    #         WIDTH / 2, HEIGHT / 2,
    #         text="Game Over\nPress 'Enter' or 'Space' button to restart",
    #         justify=tk.CENTER, font="Verdana {}".format(
    #             int(WIDTH / BLOCK_SIZE / 2)),
    #         fill="cyan")

    # def restart_the_game(self):
    #     """Перезаупуск игры"""
    #
    #     self.delete("all")
    #     self.start_speed_up_time = 0
    #     self.current_update_freq = self.default_update_freq
    #     self.score = 0
    #     self.update_text()
    #     self.blocks = [
    #         snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE, self),
    #         snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE, self),
    #         snake_components.Block(BLOCK_SIZE, BLOCK_SIZE, self)]
    #     self.snake = snake_components.Snake(self.blocks, self)
    #     if self.vanilla:
    #         self.create_food(['red'])
    #     else:
    #         self.create_food(random.choices(list(self.food_types.values()),
    #                                         weights=[DEFAULT_FOOD_PROBABILITY,
    #                                                  DOUBLE_LENGTH_PROBABILITY,
    #                                                  BOOST_PROBABILITY,
    #                                                  REVERSE_PROBABILITY]))
    #     self.level_walls = self.create_level(2)
    #     self.in_game = True
    #     self.play()

    # def update_text(self):
    #     """Обновление текста игровых очков"""
    #
    #     self.label.configure(text="Score: {0}\nHigh Score: {1}"
    #                          .format(self.score, self.high_score),
    #                          width=12, height=10)

    # def update_score(self, score):
    #     """Обновление игровых очков"""
    #
    #     self.score = self.score + score
    #     if self.score > self.high_score:
    #         self.high_score = self.high_score + score
    #     self.update_text()

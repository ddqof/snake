#!/usr/bin/env python3

import time
import tkinter as tk
import snake_components
import argparse
import random
from config import (SNAKE_SPEED, BLOCK_SIZE, WIDTH, HEIGHT,
                    DEFAULT_FOOD_PROBABILITY,
                    DOUBLE_LENGTH_PROBABILITY,
                    BOOST_PROBABILITY,
                    REVERSE_PROBABILITY)


# TODO: добавить уровни

class Driver(tk.Canvas):
    """Компонент «двигатель игры»"""

    def __init__(self, lvl, vanilla_flag, root, **kwargs):
        super(Driver, self).__init__(root, kwargs)
        self.vanilla = vanilla_flag
        self.root = root
        self.blocks = [
            snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE, BLOCK_SIZE, self)]
        self.snake = snake_components.Snake(self.blocks, self)
        self.default_update_freq = int(1 / SNAKE_SPEED * 1000)
        self.current_update_freq = self.default_update_freq
        self.start_speed_up_time = 0
        self.level_walls = []
        self.food = snake_components.Food()
        self.food_types = {0: 'red', 1: 'green', 2: 'cyan', 3: 'purple'}
        self.level_walls = self.create_level(lvl)
        if self.vanilla:
            self.create_food(['red'])
        else:
            self.create_food(random.choices((list(self.food_types.values())),
                                            weights=[DEFAULT_FOOD_PROBABILITY,
                                                     DOUBLE_LENGTH_PROBABILITY,
                                                     BOOST_PROBABILITY,
                                                     REVERSE_PROBABILITY]))
        self.score = 0
        self.high_score = 0
        self.label = tk.Label(text="Score: {0}\nHigh Score: {1}"
                              .format(self.score, self.high_score),
                              width=12, height=10)
        self.label.pack(side=tk.LEFT)
        self.bind("<KeyPress>", self.key_handle)
        self.in_game = True
        self.last_handled_vector = snake_components.Vector(1, 0)

    def play(self):
        """Запуск игрового процесса"""

        self.snake.move()
        if self.start_speed_up_time != 0:
            if int(time.perf_counter() - self.start_speed_up_time) == 3:
                self.current_update_freq = self.default_update_freq
        if self.in_game:
            self.root.after(int(self.current_update_freq), self.play)

    def create_food(self, food_colour):
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
        for block in self.blocks:
            block_coords[index] = tuple(self.coords(block.image))
            index += 1
        for lvl_block in self.level_walls:
            block_coords[index] = tuple(self.coords(lvl_block))
        if food not in block_coords.values():
            self.food.type = food_colour[0]
            self.food.image = self.create_oval(
                food[0], food[1], food[2], food[3], fill=self.food.type)
        else:
            self.create_food(food_colour)

    def create_random_wall(self):
        """Создание еды для змейки"""

        walls_count = 0
        level_walls_coords = []
        while walls_count < 50:
            block_coords = {}
            wall_x1 = BLOCK_SIZE * random.randint(
                1, BLOCK_SIZE * (WIDTH / BLOCK_SIZE ** 2) - 2)
            wall_y1 = BLOCK_SIZE * random.randint(
                1, BLOCK_SIZE * (HEIGHT / BLOCK_SIZE ** 2) - 2)
            wall_x2 = wall_x1 + BLOCK_SIZE
            wall_y2 = wall_y1 + BLOCK_SIZE
            wall = (wall_x1, wall_y1, wall_x2, wall_y2)
            for index in range(len(self.blocks)):
                block_coords[index] = tuple(self.coords(self.blocks[index].image))
            block_coords[len(self.blocks)] = tuple(self.coords(self.food))
            if wall not in block_coords.values():
                level_walls_coords.append(self.create_rectangle(
                    wall[0], wall[1], wall[2], wall[3], fill='grey'))
                walls_count += 1
        return level_walls_coords

    def create_level(self, lvl):
        walls = []
        if lvl == 1:
            for i in range(40):
                walls.append(self.create_rectangle(BLOCK_SIZE * i, 0, BLOCK_SIZE * (i + 1), BLOCK_SIZE, fill='gray'))
        if lvl == 2:
            walls = self.create_random_wall()
        return walls

    def finish_the_game(self):
        """Остановка и завершение игры"""

        self.in_game = False
        self.create_text(
            WIDTH / 2, HEIGHT / 2,
            text="Game Over\nPress 'Enter' or 'Space' button to restart",
            justify=tk.CENTER, font="Verdana {}".format(
                int(WIDTH / BLOCK_SIZE / 2)),
            fill="cyan")

    def restart_the_game(self):
        """Перезаупуск игры"""

        self.delete("all")
        self.start_speed_up_time = 0
        self.current_update_freq = self.default_update_freq
        self.score = 0
        self.update_text()
        self.blocks = [
            snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE, BLOCK_SIZE, self)]
        self.snake = snake_components.Snake(self.blocks, self)
        if self.vanilla:
            self.create_food(['red'])
        else:
            self.create_food(random.choices(list(self.food_types.values()),
                                            weights=[DEFAULT_FOOD_PROBABILITY,
                                                     DOUBLE_LENGTH_PROBABILITY,
                                                     BOOST_PROBABILITY,
                                                     REVERSE_PROBABILITY]))
        self.level_walls = self.create_level(2)
        self.in_game = True
        self.play()

    def update_text(self):
        """Обновление текста игровых очков"""

        self.label.configure(text="Score: {0}\nHigh Score: {1}"
                             .format(self.score, self.high_score),
                             width=12, height=10)

    def update_score(self, score):
        """Обновление игровых очков"""

        self.score = self.score + score
        if self.score > self.high_score:
            self.high_score = self.high_score + score
        self.update_text()

    def key_handle(self, event):
        """Обработка нажатий на клавиши"""

        key = event.keysym
        if key == 's' or key == 'Down':
            if self.snake.last_handled_vector.y == 0 and self.in_game:
                self.snake.vector = snake_components.Vector(0, 1)

        if key == 'w' or key == 'Up':
            if self.snake.last_handled_vector.y == 0 and self.in_game:
                self.snake.vector = snake_components.Vector(0, -1)

        if key == 'd' or key == 'Right':
            if self.snake.last_handled_vector.x == 0 and self.in_game:
                self.snake.vector = snake_components.Vector(1, 0)

        if key == 'a' or key == 'Left':
            if self.snake.last_handled_vector.x == 0 and self.in_game:
                self.snake.vector = snake_components.Vector(-1, 0)

        if (key == 'space' or key == 'Return') and not self.in_game:
            self.restart_the_game()


def main():
    """Подготовка к запуску игрового процесса"""

    args = parse_args()
    root = tk.Tk()
    root.title("Snake")
    game_engine = Driver(args.lvl, args.v, root,
                         width=WIDTH, height=HEIGHT, bg="black")
    game_engine.pack()
    game_engine.focus_set()
    game_engine.play()

    root.mainloop()


def parse_args():
    """Разбор аргуметов запуска"""

    parser = argparse.ArgumentParser(
        prog='snake_engine.py',
        description='''Snake game. Use W-A-S-D or Arrow keys to
        control the snake.''',
        epilog='''Author: Dmitry Podaruev <ddqof.vvv@gmail.com>'''
    )
    parser.add_argument('-v',
                        help='launch vanilla version of game',
                        action='store_true')
    parser.add_argument('-lvl',
                        type=int,
                        help='select game level',
                        default=0)
    return parser.parse_args()


if __name__ == '__main__':
    main()

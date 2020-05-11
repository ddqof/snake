#!/usr/bin/env python3

import argparse
import snake_engine
import tkinter as tk
import snake_components
from config import (SNAKE_SPEED, BLOCK_SIZE, WIDTH, HEIGHT,
                    DEFAULT_FOOD_PROBABILITY,
                    DOUBLE_LENGTH_PROBABILITY,
                    BOOST_PROBABILITY,
                    REVERSE_PROBABILITY)


class Canvas(tk.Canvas):
    """Компонент «двигатель игры»"""

    def __init__(self, driver, root, **kwargs):
        super(Canvas, self).__init__(root, kwargs)
        self.root = root
        self.driver = driver
        self.label = tk.Label(text="Score: {0}\nHigh Score: {1}"
                              .format(self.driver.score, self.driver.high_score),
                              width=12, height=10)
        self.label.pack(side=tk.LEFT)
        self.bind("<KeyPress>", self.key_handle)
        self.last_handled_vector = snake_components.Vector(1, 0)

    def drawing(self):
        self.delete('all')
        for block in self.driver.snake.blocks:
            self.create_rectangle(block.canvas_coords[0], block.canvas_coords[1], block.canvas_coords[2], block.canvas_coords[3], fill='white')
        food_coords = self.driver.food.canvas_coords
        self.create_oval(food_coords[0], food_coords[1], food_coords[2], food_coords[3], fill=self.driver.food.type)

    def play(self):
        """Запуск игрового процесса"""

        self.driver.snake.move()
        self.drawing()
        self.root.after(int(self.driver.default_update_freq), self.play)

    def key_handle(self, event):
        """Обработка нажатий на клавиши"""

        key = event.keysym
        if key == 's' or key == 'Down':
            if self.driver.snake.last_handled_vector.y == 0:
                self.driver.snake.vector = snake_components.Vector(0, 1)

        if key == 'w' or key == 'Up':
            if self.driver.snake.last_handled_vector.y == 0:
                self.driver.snake.vector = snake_components.Vector(0, -1)

        if key == 'd' or key == 'Right':
            if self.driver.snake.last_handled_vector.x == 0:
                self.driver.snake.vector = snake_components.Vector(1, 0)

        if key == 'a' or key == 'Left':
            if self.driver.snake.last_handled_vector.x == 0:
                self.driver.snake.vector = snake_components.Vector(-1, 0)

        # if (key == 'space' or key == 'Return') and not self.in_game:
        #     self.restart_the_game()


def main():
    """Подготовка к запуску игрового процесса"""

    args = parse_args()
    root = tk.Tk()
    root.title("Snake")
    game_engine = snake_engine.Driver(args.lvl, args.v)
    game_gui = Canvas(game_engine, root, width=WIDTH, height=HEIGHT, bg="black")
    game_gui.pack()
    game_gui.focus_set()
    game_gui.play()

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

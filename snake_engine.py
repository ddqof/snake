#!/usr/bin/env python3

import tkinter as tk
import snake_components
import argparse
import random
from config import SNAKE_SPEED, BLOCK_SIZE, WIDTH, HEIGHT


class Master(tk.Canvas):
    def __init__(self, root, **kwargs):
        super(Master, self).__init__(root, kwargs)
        self.root = root
        self.blocks = [
            snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE, BLOCK_SIZE, self)]
        self.snake = snake_components.Snake(self.blocks, self)
        self.food = 0
        self.create_food()
        self.bind("<KeyPress>", self.key_handle)
        self.IN_GAME = True

    def play(self):
        self.snake.move()
        if self.IN_GAME:
            self.root.after(int(1 / SNAKE_SPEED * 1000), self.play)

    def create_food(self):
        block_coords = {}
        food_x1 = BLOCK_SIZE * random.randint(
            1, BLOCK_SIZE * ((WIDTH / BLOCK_SIZE ** 2) - 1))
        food_y1 = BLOCK_SIZE * random.randint(
            1, (HEIGHT * BLOCK_SIZE) / (BLOCK_SIZE ** 2) - BLOCK_SIZE)
        food_x2 = food_x1 + BLOCK_SIZE
        food_y2 = food_y1 + BLOCK_SIZE
        food = (food_x1, food_y1, food_x2, food_y2)
        for index in range(len(self.blocks)):
            block_coords[index] = tuple(self.coords(self.blocks[index].image))
        if food not in block_coords.values():
            self.food = self.create_oval(food[0], food[1], food[2], food[3],
                                         fill="red")
        else:
            self.create_food()

    def finish_the_game(self):
        self.IN_GAME = False
        self.create_text(
            WIDTH / 2, HEIGHT / 2,
            text="Game Over\nPress 'Enter' or 'r' button to restart",
            justify=tk.CENTER, font="Verdana {}".format(
                int(WIDTH / BLOCK_SIZE / 2)),
            fill="cyan")

    def key_handle(self, event):
        if event.keycode == 83 or event.keycode == 40:
            if self.snake.vector.y == 0 and self.IN_GAME:
                self.snake.vector = snake_components.Vector(0, 1)

        if event.keycode == 87 or event.keycode == 38:
            if self.snake.vector.y == 0 and self.IN_GAME:
                self.snake.vector = snake_components.Vector(0, -1)

        if event.keycode == 68 or event.keycode == 39:
            if self.snake.vector.x == 0 and self.IN_GAME:
                self.snake.vector = snake_components.Vector(1, 0)

        if event.keycode == 65 or event.keycode == 37:
            if self.snake.vector.x == 0 and self.IN_GAME:
                self.snake.vector = snake_components.Vector(-1, 0)

        if (event.keycode == 13 or event.keycode == 82) and not self.IN_GAME:
            self.delete("all")
            self.blocks = [
                snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE, self),
                snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE, self),
                snake_components.Block(BLOCK_SIZE, BLOCK_SIZE, self)]
            self.snake = snake_components.Snake(self.blocks, self)
            self.create_food()
            self.IN_GAME = True
            self.play()


def main():
    """Запуск игрового процесса"""

    parse_args()
    root = tk.Tk()
    root.title("Snake")
    game_engine = Master(root, width=WIDTH, height=HEIGHT, bg="black")
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
    return parser.parse_args()


if __name__ == '__main__':
    main()
